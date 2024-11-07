import statistics
from collections.abc import Iterable, Mapping, Sequence
from math import sqrt
from typing import TYPE_CHECKING, Self

from pydantic.alias_generators import to_camel

from tune_nix_eval.extra_pydantic import PydanticObject

# Don't actually import this to prevent circular imports
if TYPE_CHECKING:
    from tune_nix_eval.nix.eval.raw import RawNixEvalResult


class NixEvalStats(PydanticObject, alias_generator=to_camel):
    class Envs(PydanticObject, alias_generator=to_camel):
        bytes: int
        elements: int
        number: int

    class Gc(PydanticObject, alias_generator=to_camel):
        cycles: int
        heap_size: int
        total_bytes: int

    class List(PydanticObject, alias_generator=to_camel):
        bytes: int
        concats: int
        elements: int

    class Sets(PydanticObject, alias_generator=to_camel):
        bytes: int
        elements: int
        number: int

    class Sizes(PydanticObject, alias_generator=to_camel):
        Attr: int
        Bindings: int
        Env: int
        Value: int

    class Symbols(PydanticObject, alias_generator=to_camel):
        bytes: int
        number: int

    class Time(PydanticObject, alias_generator=to_camel):
        cpu: float
        gc: float
        gc_fraction: float

    class Values(PydanticObject, alias_generator=to_camel):
        bytes: int
        number: int

    cpu_time: float
    envs: Envs
    gc: Gc
    list: List
    nr_avoided: int
    nr_exprs: int
    nr_function_calls: int
    nr_lookups: int
    nr_op_update_values_copied: int
    nr_op_updates: int
    nr_prim_op_calls: int
    nr_thunks: int
    sets: Sets
    sizes: Sizes
    symbols: Symbols
    time: Time
    values: Values


class StatsDescription(PydanticObject):
    """
    Provides a description of the statistics.
    """

    min: float
    max: float
    mean: float
    median: float
    variance: float
    std_dev: float

    @classmethod
    def of(cls: type[Self], measurements: Iterable[float]) -> Self:
        """
        Create a new instance of the class using the statistics provided.
        """
        ordered = sorted(measurements)
        n = len(ordered)
        min = ordered[0]
        max = ordered[-1]
        median = ordered[n // 2] if n % 2 == 1 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2
        mean = statistics.fmean(ordered)
        variance = statistics.variance(ordered, xbar=mean)
        std_dev = sqrt(variance)
        return cls(min=min, max=max, mean=mean, median=median, std_dev=std_dev, variance=variance)


_RawStatsDescriptionResult = Mapping[str, "StatsDescription | _RawStatsDescriptionResult"]


class NixEvalStatsDescription(PydanticObject, alias_generator=to_camel):
    class Gc(PydanticObject, alias_generator=to_camel):
        cycles: StatsDescription
        heap_size: StatsDescription
        total_bytes: StatsDescription

    class Time(PydanticObject, alias_generator=to_camel):
        cpu: StatsDescription
        gc: StatsDescription
        gc_fraction: StatsDescription

    gc: Gc
    time: Time
    wall_time: StatsDescription

    @classmethod
    def of(cls: type[Self], results: "Iterable[RawNixEvalResult]") -> Self:
        """
        Create a new instance of the class using the statistics provided.
        """
        gc_measurements: list[NixEvalStats.Gc] = []
        time_measurements: list[NixEvalStats.Time] = []
        wall_time_measurements: list[float] = []
        for result in results:
            gc_measurements.append(result.nix_stats.gc)
            time_measurements.append(result.nix_stats.time)
            wall_time_measurements.append(result.wall_time)

        # measurements cannot be consumed twice
        del results

        def mkStatsDescription[T: PydanticObject](
            cls: type[T], measurements: Sequence[T]
        ) -> dict[str, StatsDescription]:
            kwargs: dict[str, StatsDescription] = {}
            for key, field_info in cls.model_fields.items():
                if field_info.annotation is None:
                    raise TypeError(f"Field {key} has no annotation")
                elif issubclass(field_info.annotation, (int, float)):
                    kwargs[key] = StatsDescription.of(getattr(measurement, key) for measurement in measurements)
                else:
                    raise TypeError(f"Field {key} has an invalid annotation")
            return kwargs

        return cls.model_validate({
            "gc": mkStatsDescription(NixEvalStats.Gc, gc_measurements),
            "time": mkStatsDescription(NixEvalStats.Time, time_measurements),
            "wall_time": StatsDescription.of(wall_time_measurements),
        })
