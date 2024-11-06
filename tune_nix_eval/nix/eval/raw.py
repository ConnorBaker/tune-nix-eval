import json
import os
import threading
import time
from collections.abc import Iterable, Mapping, Sequence
from logging import Logger
from subprocess import PIPE
from tempfile import NamedTemporaryFile
from typing import Any, Final

import psutil
from pydantic.alias_generators import to_camel

from tune_nix_eval.extra_pydantic import PydanticObject
from tune_nix_eval.logger import get_logger
from tune_nix_eval.nix.eval.stats import NixEvalStats
from tune_nix_eval.nix.utilities import show_attr_path

LOGGER: Final[Logger] = get_logger(__name__)


class MemoryProcessStats(PydanticObject):
    rss: int
    vms: int
    uss: int
    pss: int
    swap: int


class RawNixEvalResult(PydanticObject, alias_generator=to_camel):
    memory_stats: Sequence[MemoryProcessStats]
    stats: NixEvalStats
    stderr: str
    value: Any  # JSON object


# Function to monitor memory usage
# NOTE: Mutates memory_stats!
def monitor_memory(pid: int, memory_stats: list[MemoryProcessStats], interval: float = 1.0) -> None:
    assert memory_stats == []

    process = psutil.Process(pid)
    while process.is_running():
        # Process may have been terminated between is_running() and memory_full_info()
        try:
            mem_info = process.memory_full_info()
        except psutil.NoSuchProcess:
            break
        memory_stats.append(MemoryProcessStats.model_validate(mem_info, from_attributes=True))
        time.sleep(interval)


def eval(
    flakeref: str,
    attr_path: Iterable[str],
    local_store: bool = False,
    env: Mapping[str, str] = {},
) -> RawNixEvalResult:
    # TODO: Escaping of flakeref and attr_path is correct?
    full_ref: str = f"{flakeref}#{show_attr_path(attr_path)}"
    LOGGER.info("Evaluating %s", full_ref)

    kwargs = {}
    with NamedTemporaryFile() as stats_file:
        proc = psutil.Popen(
            args=[
                "nix",
                "eval",
                # Configuration options
                # TODO(@connorbaker): Disabled for now.
                # "--no-allow-import-from-derivation",
                # "--no-allow-unsafe-native-code-during-evaluation",
                # "--pure-eval",
                # "--read-only",
                "--no-eval-cache",
                "--store",
                ("local" if local_store else "auto"),
                "--eval-store",
                ("local" if local_store else "auto"),
                # Prevent remote builders when doing IFD
                "--builders",
                "''",
                # Output format
                "--json",
                # Evaluation target
                full_ref,
            ],
            stdout=PIPE,
            stderr=PIPE,
            env=os.environ | env | {"NIX_SHOW_STATS": "1", "NIX_SHOW_STATS_PATH": stats_file.name},
        )

        # Limit CPU affinity to the first core
        proc.cpu_affinity([0])

        # Start monitoring memory usage
        # NOTE: memory_stats is mutated by monitor_memory.
        memory_stats: list[MemoryProcessStats] = []
        monitor_thread = threading.Thread(
            target=monitor_memory,
            args=(
                proc.pid,
                memory_stats,
            ),
        )
        monitor_thread.start()

        # Wait for the process to finish
        proc.wait()

        # Stop monitoring memory usage
        monitor_thread.join()

        kwargs["memory_stats"] = memory_stats
        kwargs["stats"] = NixEvalStats.model_validate_json(stats_file.read())
        kwargs["stderr"] = str(proc.stderr)
        if proc.returncode != 0:
            LOGGER.error("Evaluation failed: %s", kwargs["stderr"])
            kwargs["value"] = None
        else:
            kwargs["value"] = json.load(proc.stdout)

    return RawNixEvalResult.model_validate(kwargs)
