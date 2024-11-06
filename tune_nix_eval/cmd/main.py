from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from functools import partial
from logging import Logger
from typing import Final, cast

import optuna
from optuna.samplers import BruteForceSampler
from optuna.trial import Trial

import tune_nix_eval.nix.build.raw
import tune_nix_eval.nix.eval.raw
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


def objective(num_evals: int, flakeref: str, attr_path: Sequence[str], trial: Trial) -> float:
    env: dict[str, str] = {
        # "GC_INITIAL_HEAP_SIZE": str(gc_initial_heap_size),
        # "GC_FREE_SPACE_DIVISOR": str(gc_free_space_divisor),
    }

    # NOTE: Boehm GC just checks if the environment variable is set, not that it is set to a specific value.
    gc_dont_gc = trial.suggest_categorical("gc_dont_gc", [True, False])
    if gc_dont_gc:
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

    memory_allocator: MemoryAllocator = cast(
        MemoryAllocator, trial.suggest_categorical("memory_allocator", sorted(MemoryAllocators))
    )
    env["LD_PRELOAD"] = get_memory_allocator_ld_preload(memory_allocator)

    # Short-circuit if the trial is a duplicate.
    # Fetch all the trials to consider.
    # for t in reversed(trial.study.get_trials(deepcopy=False, states=(TrialState.COMPLETE,))):
    #     # TODO: Match on `t.state` and set state of new trial appropriately.
    #     if trial.params == t.params and t.value is not None:
    #         # Use the existing value as trial duplicated the parameters.
    #         return t.value

    results: list[RawNixEvalResult] = []
    for i in range(num_evals):
        LOGGER.info("Running evaluation %d of %d", i + 1, num_evals)
        intermediate_result = tune_nix_eval.nix.eval.raw.eval(flakeref, attr_path, env=env)
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
    trial.set_user_attr("stats", description.model_dump(mode="json"))
    return description.time.cpu.median


def main() -> None:
    parser = setup_argparse()
    args: Namespace = parser.parse_args()
    flakeref = args.flakeref
    attr_path = args.attr_path

    # Setup
    LOGGER.info("Building memory allocators")
    build_memory_allocators()

    # Warmup
    LOGGER.info("Warming up")
    _ = tune_nix_eval.nix.eval.raw.eval(flakeref, attr_path)

    optuna.logging.get_logger("optuna").addHandler(_HANDLER)
    study = optuna.create_study(
        direction="minimize",
        storage="sqlite:///example.db",
        study_name="nix-eval",
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
    study.enqueue_trial({"memory_allocator": "system", "gc_dont_gc": False})

    objective_wrapper = partial(objective, args.num_evals, flakeref, attr_path)

    study.optimize(objective_wrapper, n_trials=args.num_trials)

    print(study.best_params)
