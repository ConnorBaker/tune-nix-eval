import json
import multiprocessing
import multiprocessing.process
import os
import time
from collections.abc import Iterable, Mapping, Sequence
from logging import Logger
from subprocess import PIPE
from tempfile import NamedTemporaryFile
from typing import Any, Final, overload

import psutil
from pydantic.alias_generators import to_camel

from tune_nix_eval.extra_pydantic import PydanticObject
from tune_nix_eval.logger import get_logger
from tune_nix_eval.nix.eval.stats import NixEvalStats
from tune_nix_eval.nix.utilities import show_attr_path

LOGGER: Final[Logger] = get_logger(__name__)


class ProcessStats(PydanticObject, extra="ignore"):
    class Cpu(PydanticObject, extra="ignore"):
        user: float
        system: float
        children_user: float
        children_system: float
        iowait: float

    class Io(PydanticObject, extra="ignore"):
        read_count: int
        write_count: int
        read_bytes: int
        write_bytes: int
        read_chars: int
        write_chars: int

    class Memory(PydanticObject, extra="ignore"):
        rss: int
        vms: int
        uss: int
        pss: int
        swap: int

    cpu: Cpu
    io: None | Io
    memory: Memory
    time: float


class RawNixEvalResult(PydanticObject, alias_generator=to_camel):
    nix_stats: NixEvalStats
    process_stats: Sequence[ProcessStats]
    stderr: str
    wall_time: float
    value: Any  # JSON object


# Function to monitor memory usage
# NOTE: Mutates memory_stats!
def monitor_process(
    pid: int,
    process_stats: list[ProcessStats],
    interval: float = 1.0,
) -> None:
    process = psutil.Process(pid)
    while process.is_running():
        # Process may have been terminated between is_running() and as_dict()
        try:
            info = process.as_dict(
                attrs=[
                    "cpu_times",
                    "create_time",
                    "io_counters",
                    "memory_full_info",
                ]
            )
        except psutil.NoSuchProcess:
            break

        info["cpu"] = info.pop("cpu_times")._asdict()
        # Sometimes we don't have IO counters
        info["io"] = io_counters._asdict() if (io_counters := info.pop("io_counters", None)) is not None else None
        info["memory"] = info.pop("memory_full_info")._asdict()
        info["time"] = time.time() - info.pop("create_time")

        process_stats.append(ProcessStats.model_validate(info))
        time.sleep(interval)


@overload
def eval(
    flakeref: str,
    attr_path: Iterable[str],
    local_store: bool = False,
    env: Mapping[str, str] = {},
    timeout: None = ...,
) -> RawNixEvalResult: ...


@overload
def eval(
    flakeref: str,
    attr_path: Iterable[str],
    local_store: bool = False,
    env: Mapping[str, str] = {},
    timeout: float = ...,
) -> None | RawNixEvalResult: ...


def eval(
    flakeref: str,
    attr_path: Iterable[str],
    local_store: bool = False,
    env: Mapping[str, str] = {},
    timeout: None | float = None,
) -> None | RawNixEvalResult:
    # TODO: Escaping of flakeref and attr_path is correct?
    full_ref: str = f"{flakeref}#{show_attr_path(attr_path)}"
    LOGGER.info("Evaluating %s", full_ref)

    kwargs = {}
    with NamedTemporaryFile() as stats_file, multiprocessing.Manager() as manager:
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
                # Store options
                *(["--store", "local", "--eval-store", "local"] if local_store else []),
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
        process_stats = manager.list()
        monitor = multiprocessing.Process(target=monitor_process, args=(proc.pid, process_stats))

        # Wait for the process to finish
        try:
            monitor.start()
            returncode = proc.wait(timeout)
            monitor.join(timeout)  # Re-use timeout here as a default, although it should be much faster
        except psutil.TimeoutExpired:
            LOGGER.error("Evaluation timed out")
            proc.kill()
            monitor.terminate()
            return None

        # Convert back to normal list
        kwargs["process_stats"] = list(process_stats)
        kwargs["nix_stats"] = NixEvalStats.model_validate_json(stats_file.read())
        kwargs["stderr"] = str(proc.stderr.read())
        kwargs["wall_time"] = time.time() - proc.create_time()
        LOGGER.info("Evaluation completed in %.2fs", kwargs["wall_time"])
        if returncode != 0:
            LOGGER.error("Evaluation failed: %s", kwargs["stderr"])
            kwargs["value"] = None
        else:
            kwargs["value"] = json.load(proc.stdout)

    return RawNixEvalResult.model_validate(kwargs)
