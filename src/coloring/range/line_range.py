from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from coloring.range.ABCs import LineRangeABC, RangeABC
from coloring.range.range import get_range_object
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class Length(LineRangeABC):
    min_length: float
    max_length: float
    range: RangeABC

    @classmethod
    def from_json(
        cls,
        min_length: float,
        max_length: float,
        range: dict[str, Any]
    ) -> Length:
        return cls(
            min_length, max_length, get_range_object(range)
        )

    def get_value(self, edge: Edge, t: float) -> float:
        length = edge.length()
        t = (length - self.min_length) / (self.max_length - self.min_length)
        t = max(0.0, min(t, 1.0))
        t = self.range.get_value(t)
        return t


def get_line_range_object(configs: dict[str, Any] | ObjectConfigs) -> LineRangeABC:
    return get_object(LineRangeABC, configs)
