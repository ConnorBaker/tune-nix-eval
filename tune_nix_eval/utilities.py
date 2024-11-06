# NOTE: Open bugs in Pydantic like https://github.com/pydantic/pydantic/issues/8984 prevent the full switch to the type
# keyword introduced in Python 3.12.
import base64
from hashlib import sha256

from tune_nix_eval.extra_types import (
    Sha256,
    SriHash,
    SriHashTA,
)


def sha256_bytes_to_sri_hash(sha256_bytes: bytes) -> SriHash:
    base64_hash = base64.b64encode(sha256_bytes).decode("utf-8")
    sri_hash = f"sha256-{base64_hash}"
    return SriHashTA.validate_strings(sri_hash)


def sha256_to_sri_hash(sha256: Sha256) -> SriHash:
    """
    Convert a Base16 SHA-256 hash to a Subresource Integrity (SRI) hash.
    """
    return sha256_bytes_to_sri_hash(bytes.fromhex(sha256))


def mk_sri_hash(bs: bytes) -> SriHash:
    """
    Compute a Subresource Integrity (SRI) hash from a byte string.
    """
    return sha256_bytes_to_sri_hash(sha256(bs).digest())
