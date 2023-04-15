from dataclasses import dataclass, field
from typing import Any, Optional

from coloring.ABCs import LineRangeABC, RangeABC
from coloring.range import get_range_object
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class Length(LineRangeABC):
    min_length: float
    max_length: float
    range: dict[str, Any] = field(default_factory=dict)
    _range: Optional[RangeABC] = field(init=False)

    def __post_init__(self) -> None:
        self._range = get_range_object(self.range)

    def get_value(self, edge: Edge, t: float) -> float:
        length = edge.length()
        t = (length - self.min_length) / (self.max_length - self.min_length)
        t = max(0.0, min(t, 1.0))
        if self._range is not None:
            t = self._range.get_value(t)
        return t
    

def get_line_range_object(configs: dict[str, Any] | ObjectConfigs) -> Optional[LineRangeABC]:
    return get_object(LineRangeABC, configs)
