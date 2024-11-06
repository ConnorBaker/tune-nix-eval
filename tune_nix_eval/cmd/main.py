from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path
from typing import Final, cast

import optuna
from optuna.artifacts import FileSystemArtifactStore, upload_artifact
from optuna.samplers import BruteForceSampler
from optuna.trial import Trial

import tune_nix_eval.nix.build.raw
import tune_nix_eval.nix.eval.raw
from tune_nix_eval.extra_pydantic import PydanticObject
from tune_nix_eval.logger import _HANDLER, get_logger
from tune_nix_eval.memory_allocators import (
    MemoryAllocator,
    MemoryAllocators,
    build_memory_allocators,
    get_memory_allocator_ld_preload,
)
from tune_nix_eval.nix.eval.raw import RawNixEvalResult
from tune_nix_eval.nix.eval.stats import NixEvalStatsDescription

LOGGER: Final[Logger] = get_logger(__name__)


# TODO(@connorbaker):
# 0. Set CPU governor to performance to avoid fluctuations in CPU frequency.
# 1. Tune zram and compression algorithm parameters
# 2. Visualizations of memory usage (add snapshot time relative to program start to memory_stats)


def setup_argparse() -> ArgumentParser:
    parser = ArgumentParser(description="Does a thing")
    _ = parser.add_argument(
        "--num-trials",
        type=int,
        help="Number of trials",
        default=10,
    )
    _ = parser.add_argument(
        "--num-evals",
        type=int,
        help="Max number of evaluations per trial",
        default=5,
    )
    _ = parser.add_argument(
        "--allow-turbo",
        action="store_true",
        help="Allow the CPU to boost its frequency. Recommended to disable for consistent results.",
        default=False,
    )
    _ = parser.add_argument(
        "--tune-store",
        action="store_true",
        help="Test both with and without the Nix daemon. Requires the current user to own the Nix store!",
        default=False,
    )
    _ = parser.add_argument(
        "--flakeref",
        type=str,
        help="Reference to a flake",
        required=True,
    )
    _ = parser.add_argument(
        "--attr-path",
        type=str,
        nargs="+",
        help="Attribute to evaluate",
        required=True,
    )
    return parser


class NixEvalResults(PydanticObject):
    results: Sequence[RawNixEvalResult]
    description: NixEvalStatsDescription


@dataclass(frozen=True, slots=True, eq=True, order=True)
class Objective:
    flakeref: str
    attr_path: Sequence[str]
    num_evals: int
    tune_store: bool
    artifact_dir: Path

    artifact_store: FileSystemArtifactStore = field(init=False, repr=False, hash=False, compare=False)

    # Work around immutability in a gross way.
    def __post_init__(self) -> None:
        object.__setattr__(self, "artifact_store", FileSystemArtifactStore(self.artifact_dir))

    def __call__(self, trial: Trial) -> float:
        env: dict[str, str] = {}

        bypass_daemon = (
            trial.suggest_categorical("bypass_daemon", (["true"] if self.tune_store else []) + ["false"]) == "true"
        )

        # NOTE: Boehm GC just checks if the environment variable is set, not that it is set to a specific value.
        # TODO: Web dashboard struggles with booleans? Seeing empty spaces in the table.
        if trial.suggest_categorical("gc_dont_gc", ["true", "false"]) == "true":
            env["GC_DONT_GC"] = "1"

        # Measured in bytes -- 32M through 8G
        # gc_initial_heap_size = trial.suggest_int("gc_initial_heap_size", 32 * 1024 * 1024, 8 * 1024 * 1024 * 1024, log=True)
        # env["GC_INITIAL_HEAP_SIZE"] = str(gc_initial_heap_size)

        # GC_MAXIMUM_HEAP_SIZE is zero by default, which means unlimited.

        # GC_FREE_SPACE_DIVISOR is 3 by default.
        # From the docs:
        #   The global variable `GC_free_space_divisor` may be adjusted up from it
        #   default value of 3 to use less space and more collection time, or down for
        #   the opposite effect.  Setting it to 1 will almost disable collections
        #   and cause all allocations to simply grow the heap.
        # gc_free_space_divisor = trial.suggest_int("gc_free_space_divisor", 1, 5)
        # env["GC_FREE_SPACE_DIVISOR"] = str(gc_free_space_divisor)

        # GC_ENABLE_INCREMENTAL is off by default.
        # gc_enable_incremental = trial.suggest_categorical("gc_enable_incremental", [True, False])

        env["LD_PRELOAD"] = get_memory_allocator_ld_preload(
            cast(MemoryAllocator, trial.suggest_categorical("memory_allocator", sorted(MemoryAllocators)))
        )

        # Short-circuit if the trial is a duplicate.
        # Fetch all the trials to consider.
        # for t in reversed(trial.study.get_trials(deepcopy=False, states=(TrialState.COMPLETE,))):
        #     # TODO: Match on `t.state` and set state of new trial appropriately.
        #     if trial.params == t.params and t.value is not None:
        #         # Use the existing value as trial duplicated the parameters.
        #         return t.value

        results: list[RawNixEvalResult] = []
        for i in range(self.num_evals):
            LOGGER.info("Running evaluation %d of %d", i + 1, self.num_evals)
            intermediate_result = tune_nix_eval.nix.eval.raw.eval(
                self.flakeref, self.attr_path, local_store=bypass_daemon, env=env
            )
            if intermediate_result.value is None:
                LOGGER.error("Evaluation failed: %s", intermediate_result.stderr)
                trial.set_user_attr("stderr", intermediate_result.stderr)
                raise optuna.TrialPruned()

            # if trial.should_prune():
            #     raise optuna.TrialPruned()

            trial.report(intermediate_result.stats.time.cpu, i)
            results.append(intermediate_result)

        LOGGER.info("Generating statistics")
        description = NixEvalStatsDescription.of(result.stats for result in results)

        LOGGER.info("Creating artifact")
        eval_results = NixEvalResults(results=results, description=description)

        file_path = self.artifact_dir / f"trial-{trial.number}-eval-results.json"
        LOGGER.info("Saving statistics to %s", file_path)
        file_path.write_text(eval_results.model_dump_json())

        LOGGER.info("Uploading artifact")
        artifact_id = upload_artifact(
            artifact_store=self.artifact_store, file_path=file_path.as_posix(), study_or_trial=trial
        )

        trial.set_user_attr("artifact_id", artifact_id)
        return description.time.cpu.median


def main() -> None:
    parser = setup_argparse()
    args: Namespace = parser.parse_args()
    flakeref = args.flakeref
    attr_path = args.attr_path

    # TODO(@connorbaker):
    # echo "1" | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo
    no_turbo_path = Path("/sys/devices/system/cpu/intel_pstate/no_turbo")
    if not args.allow_turbo and no_turbo_path.exists() and no_turbo_path.read_text().strip() != "1":
        LOGGER.error("Turbo mode is enabled. Results will not be accurate.")
        LOGGER.error("Disable turbo mode with: echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo")
        raise RuntimeError("Turbo mode is enabled. Results will not be accurate.")

    LOGGER.info("Setting up artifact directory")
    artifact_dir = Path("artifacts")
    artifact_dir.mkdir(exist_ok=True)

    # Setup
    LOGGER.info("Building memory allocators")
    build_memory_allocators()

    # Warmup
    LOGGER.info("Warming up")
    _ = tune_nix_eval.nix.eval.raw.eval(flakeref, attr_path)

    optuna.logging.get_logger("optuna").addHandler(_HANDLER)
    study = optuna.create_study(
        direction="minimize",
        storage="sqlite:///nix-eval.db",
        study_name="nix-eval",
        # TODO(@connorbaker):
        # Swithc to Wilcoxon pruner since it is appropriate for objective functions which average multiple evaluations.
        # https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/013_wilcoxon_pruner.html#sphx-glr-tutorial-20-recipes-013-wilcoxon-pruner-py
        # pruner=MedianPruner(
        #     # Start pruning essentially immediately since we have our baseline trial enqueued.
        #     n_startup_trials=1,
        #     # Start pruning decisions on the third step of a trial
        #     n_warmup_steps=2,
        # ),
        # sampler=TPESampler(seed=42),
        sampler=BruteForceSampler(seed=42),
    )

    LOGGER.info("Adding baseline trial")
    # study.enqueue_trial({
    #     # https://github.com/ivmai/bdwgc/blob/462a6cd30b5d295d03b248a2aba331dcf67c8048/alloc.c#L225
    #     "gc_free_space_divisor": 3,
    #     # https://github.com/NixOS/nix/blob/dfd0033afbbb12e6578ab3f1f026d15ff9dec132/src/libexpr/eval-gc.cc#L65
    #     "gc_initial_heap_size": 32 * 1024 * 1024,
    # })
    study.enqueue_trial({"memory_allocator": "system", "gc_dont_gc": "false", "bypass_daemon": "false"})

    study.optimize(
        Objective(
            flakeref,
            attr_path,
            args.num_evals,
            args.tune_store,
            artifact_dir,
        ),
        n_trials=args.num_trials,
    )

    print(study.best_params)
