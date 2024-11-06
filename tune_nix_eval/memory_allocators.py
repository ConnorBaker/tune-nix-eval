from collections.abc import Sequence, Set
from logging import Logger
from typing import Final, Literal, overload

import tune_nix_eval.nix.build.raw
import tune_nix_eval.nix.eval.raw
from tune_nix_eval.logger import get_logger

LOGGER: Final[Logger] = get_logger(__name__)


SystemProvidedMemoryAllocator = Literal["system"]
SystemProvidedMemoryAllocators: Set[SystemProvidedMemoryAllocator] = set(SystemProvidedMemoryAllocator.__args__)
NixProvidedMemoryAllocator = Literal[
    "graphene-hardened-light",
    "graphene-hardened",
    "hoard",
    "jemalloc",
    "libc",
    "mimalloc",
    "scudo-14",
    "scudo-19",
    "tcmalloc",
]
NixProvidedMemoryAllocators: Set[NixProvidedMemoryAllocator] = set(NixProvidedMemoryAllocator.__args__)
MemoryAllocator = SystemProvidedMemoryAllocator | NixProvidedMemoryAllocator
MemoryAllocators: Set[MemoryAllocator] = SystemProvidedMemoryAllocators | NixProvidedMemoryAllocators


@overload
def get_memory_allocator_attr_path(memory_allocator: SystemProvidedMemoryAllocator) -> None: ...


@overload
def get_memory_allocator_attr_path(memory_allocator: NixProvidedMemoryAllocator) -> Sequence[str]: ...


def get_memory_allocator_attr_path(memory_allocator: MemoryAllocator) -> None | Sequence[str]:
    match memory_allocator:
        case "graphene-hardened-light" | "graphene-hardened":
            return ["graphene-hardened-malloc"]
        case "hoard":
            return ["hoard"]
        case "jemalloc":
            return ["jemalloc"]
        case "libc":
            return ["glibc"]
        case "mimalloc":
            return ["mimalloc"]
        case "scudo-14":
            return ["llvmPackages_14", "compiler-rt"]
        case "scudo-19":
            return ["llvmPackages_19", "compiler-rt"]
        case "system":
            return None
        case "tcmalloc":
            return ["gperftools"]


@overload
def get_memory_allocator_lib_path(memory_allocator: SystemProvidedMemoryAllocator) -> None: ...


@overload
def get_memory_allocator_lib_path(memory_allocator: NixProvidedMemoryAllocator) -> str: ...


def get_memory_allocator_lib_path(memory_allocator: MemoryAllocator) -> None | str:
    match memory_allocator:
        case "graphene-hardened-light":
            return "lib/libhardened_malloc-light.so"
        case "graphene-hardened":
            return "lib/libhardened_malloc.so"
        case "hoard":
            return "lib/libhoard.so"
        case "jemalloc":
            return "lib/libjemalloc.so"
        case "libc":
            # NOTE: Cannot LD_PRELOAD libc.so (invalid ELF header) -- must use libc.so.6.
            return "lib/libc.so.6"
        case "mimalloc":
            return "lib/libmimalloc.so"
        case "scudo-14":
            return "lib/linux/libclang_rt.scudo-x86_64.so"
        case "scudo-19":
            return "lib/linux/libclang_rt.scudo_standalone-x86_64.so"
        case "system":
            return None
        case "tcmalloc":
            return "lib/libtcmalloc.so"


@overload
def ensure_memory_allocator_store_path(memory_allocator: SystemProvidedMemoryAllocator) -> None: ...


@overload
def ensure_memory_allocator_store_path(memory_allocator: NixProvidedMemoryAllocator) -> str: ...


def ensure_memory_allocator_store_path(memory_allocator: MemoryAllocator) -> None | str:
    """
    Builds and returns the store path to the memory allocator, or None if the memory allocator is system.
    """
    if memory_allocator == "system":
        return None

    result = tune_nix_eval.nix.build.raw.build(".", get_memory_allocator_attr_path(memory_allocator))
    return result.value.outputs["out"]


@overload
def get_memory_allocator_ld_preload(memory_allocator: SystemProvidedMemoryAllocator) -> Literal[""]: ...


@overload
def get_memory_allocator_ld_preload(memory_allocator: NixProvidedMemoryAllocator) -> str: ...


def get_memory_allocator_ld_preload(memory_allocator: MemoryAllocator) -> str:
    if memory_allocator == "system":
        return ""

    store_path = ensure_memory_allocator_store_path(memory_allocator)
    lib_path = get_memory_allocator_lib_path(memory_allocator)
    return f"{store_path}/{lib_path}"


def build_memory_allocators() -> None:
    for memory_allocator in NixProvidedMemoryAllocators:
        LOGGER.info("Building %s", memory_allocator)
        store_path = ensure_memory_allocator_store_path(memory_allocator)
        LOGGER.info("Built %s to %s", memory_allocator, store_path)
