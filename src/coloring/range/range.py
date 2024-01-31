from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from coloring.range.ABCs import RangeABC
from configs import ObjectConfigs
from utils.concrete_inheritors import get_object
from utils.interpolate import interpolate


@dataclass
class Linear(RangeABC):

    @classmethod
    def from_json(cls) -> Linear:
        return cls()

    def get_value(self, t: float) -> float:
        return t


@dataclass
class Exponential(RangeABC):
    alpha: float

    @classmethod
    def from_json(cls, alpha: float = 1.0) -> Exponential:
        return cls(alpha)

    def get_value(self, t: float) -> float:
        t = (math.exp(self.alpha * t) - 1) / (math.exp(self.alpha) - 1)
        return t


@dataclass
class Discrete(RangeABC):
    segments: int
    range: RangeABC

    @classmethod
    def from_json(
        cls,
        segments: int,
        range: dict[str, Any]
    ) -> Discrete:
        return cls(
            segments,
            get_range_object(range)
        )

    def get_value(self, t: float) -> float:
        t = self.range.get_value(t)
        t *= self.segments
        t = int(t)
        t /= self.segments - 1
        return t


@dataclass
class EaseInOut(RangeABC):
    degree: int

    @classmethod
    def from_json(cls, degree: int = 2) -> EaseInOut:
        return cls(degree)

    def get_value(self, t: float) -> float:
        ease_in = lambda x: math.pow(x, self.degree)
        ease_out = lambda x: 1 - math.pow(1 - x, self.degree)
        return interpolate(ease_in(t), ease_out(t), t)


def get_range_object(configs: dict[str, Any] | ObjectConfigs) -> RangeABC:
    return get_object(RangeABC, configs)
