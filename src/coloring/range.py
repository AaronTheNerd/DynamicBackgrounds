import math
from dataclasses import dataclass, field
from typing import Any

from coloring.ABCs import RangeABC
from configs import ObjectConfigs
from utils.concrete_inheritors import get_object
from utils.interpolate import interpolate


@dataclass
class Linear(RangeABC):
    def get_value(self, t: float) -> float:
        return t


@dataclass
class Exponential(RangeABC):
    alpha: float = 1.0

    def get_value(self, t: float) -> float:
        t = (math.exp(self.alpha * t) - 1) / (math.exp(self.alpha) - 1)
        return t


@dataclass
class Discrete(RangeABC):
    segments: int
    range: dict[str, Any]
    _range: RangeABC = field(init=False)

    def __post_init__(self) -> None:
        self._range = get_object(RangeABC, self.range)

    def get_value(self, t: float) -> float:
        t = self._range.get_value(t)
        t *= self.segments
        t = int(t)
        t /= self.segments - 1
        return t
    

@dataclass
class EaseInOut(RangeABC):
    degree: int = 2

    def get_value(self, t: float) -> float:
        ease_in = lambda x: math.pow(t, self.degree)
        ease_out = lambda x: 1 - math.pow(1 - t, self.degree)
        return interpolate(ease_in(t), ease_out(t), t)


def get_range_object(configs: dict[str, Any] | ObjectConfigs) -> RangeABC:
    return get_object(RangeABC, configs)
