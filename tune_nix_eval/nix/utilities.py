import json
import re
from collections.abc import Iterable
from logging import Logger
from typing import Final

from tune_nix_eval.logger import get_logger

LOGGER: Final[Logger] = get_logger(__name__)


def escape_nix_string(s: str) -> str:
    # https://github.com/NixOS/nixpkgs/blob/0600d5d4a29a9f826f880f611b1e354c77128ecc/lib/strings.nix#L1211-L1236
    return json.dumps(s, check_circular=False).replace("$", "\\$")


def escape_nix_identifier(s: str) -> str:
    # https://github.com/NixOS/nixpkgs/blob/0600d5d4a29a9f826f880f611b1e354c77128ecc/lib/strings.nix#L1265-L1296
    pattern = re.compile(r"[a-zA-Z_][a-zA-Z0-9_'-]*")
    return s if pattern.match(s) else escape_nix_string(s)


def show_attr_path(attr_path: Iterable[str]) -> str:
    # https://github.com/NixOS/nixpkgs/blob/8f0377b2b83c3ff5d1670f2dff5e6388cc4deb84/lib/attrsets.nix#L1726-L1761
    return ".".join(map(escape_nix_identifier, attr_path)) if attr_path else "<root attribute path>"
