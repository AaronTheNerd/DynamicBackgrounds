import math
from dataclasses import dataclass
from typing import Any

from coloring.ABCs import ReflectiveRangeABC
from configs import ObjectConfigs
from utils.concrete_inheritors import get_object


@dataclass
class Sine(ReflectiveRangeABC):
    frequency: int = 1

    def get_value(self, t: float) -> float:
        return (math.sin(t * self.frequency * 2 * math.pi) + 1) / 2
    

@dataclass
class Cosine(ReflectiveRangeABC):
    frequency: int = 1

    def get_value(self, t: float) -> float:
        return (math.cos(t * self.frequency * 2 * math.pi) + 1) / 2


@dataclass
class Linear(ReflectiveRangeABC):
    def get_value(self, t: float) -> float:
        return 2 * t if t <= 0.5 else (1 - t) * 2


def get_reflective_range_object(configs: ObjectConfigs | dict[str, Any]) -> ReflectiveRangeABC:
    return get_object(ReflectiveRangeABC, configs)