import json
import os
from collections.abc import Iterable, Mapping
from logging import Logger
from subprocess import run
from tempfile import NamedTemporaryFile
from typing import Final

from pydantic.alias_generators import to_camel

from tune_nix_eval.extra_pydantic import PydanticObject
from tune_nix_eval.logger import get_logger
from tune_nix_eval.nix.eval.stats import NixEvalStats
from tune_nix_eval.nix.utilities import show_attr_path

LOGGER: Final[Logger] = get_logger(__name__)


class NixBuildResult(PydanticObject, alias_generator=to_camel):
    class NixBuildResultSingleton(PydanticObject, alias_generator=to_camel):
        drv_path: str
        outputs: Mapping[str, str]

    stderr: str
    value: NixBuildResultSingleton


def build(flakeref: str, attr_path: Iterable[str], output: str = "*") -> NixBuildResult:
    # TODO: Escaping of flakeref and attr_path is correct?
    full_ref: str = f"{flakeref}#{show_attr_path(attr_path)}^{output}"
    LOGGER.info("Building %s", full_ref)

    kwargs = {}
    proc = run(
        args=[
            "nix",
            "build",
            # Configuration options
            "--no-allow-import-from-derivation",
            "--no-allow-unsafe-native-code-during-evaluation",
            "--pure-eval",
            "--no-link",
            # Output format
            "--json",
            # Build target
            full_ref,
        ],
        capture_output=True,
        check=False,
        env=os.environ,
    )
    kwargs["stderr"] = proc.stderr.decode()
    if proc.returncode != 0:
        LOGGER.error("Evaluation failed: %s", kwargs["stderr"])
        kwargs["value"] = None
    else:
        kwargs["value"] = json.loads(proc.stdout)

    match kwargs["value"]:
        case [value]:
            kwargs["value"] = value
        case _:
            LOGGER.error("Expected singleton list output, but recieved: %s", kwargs["value"])
            raise ValueError("Unexpected output")

    return NixBuildResult.model_validate(kwargs)
