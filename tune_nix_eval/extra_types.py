# NOTE: Open bugs in Pydantic like https://github.com/pydantic/pydantic/issues/8984 prevent the full switch to the type
# keyword introduced in Python 3.12.
from typing import (
    Annotated,
    Final,
)

from pydantic import Field, TypeAdapter

from tune_nix_eval.extra_pydantic import PydanticTypeAdapter

Md5 = Annotated[
    str,
    Field(
        description="An MD5 hash.",
        examples=["0123456789abcdef0123456789abcdef"],
        pattern=r"[0-9a-f]{32}",
    ),
]
Md5TA: Final[TypeAdapter[Md5]] = PydanticTypeAdapter(Md5)

Sha256 = Annotated[
    str,
    Field(
        description="A SHA256 hash.",
        examples=["0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"],
        pattern=r"[0-9a-f]{64}",
    ),
]
Sha256TA: Final[TypeAdapter[Sha256]] = PydanticTypeAdapter(Sha256)

SriHash = Annotated[
    str,
    Field(
        description="An SRI hash.",
        examples=["sha256-LxcXgwe1OCRfwDsEsNLIkeNsOcx3KuF5Sj+g2dY6WD0="],
        pattern=r"(?<algorithm>md5|sha1|sha256|sha512)-[A-Za-z0-9+/]+={0,2}",
    ),
]
SriHashTA: Final[TypeAdapter[SriHash]] = PydanticTypeAdapter(SriHash)
