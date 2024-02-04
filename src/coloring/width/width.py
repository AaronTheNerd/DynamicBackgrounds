from __future__ import annotations

from dataclasses import dataclass

from coloring.width.ABCs import WidthABC
from configs import ObjectConfigs
from serial.JSON_types import JSON_object
from utils.concrete_inheritors import get_object


@dataclass
class Static(WidthABC):
    width: int

    @classmethod
    def from_json(cls, *args, **kwargs) -> Static:
        return cls(*args, **kwargs)

    def get_width(self, t: float, time: float) -> int:
        return self.width


@dataclass
class Range(WidthABC):
    min_width: int
    max_width: int

    @classmethod
    def from_json(cls, *args, **kwargs) -> Range:
        return cls(*args, **kwargs)

    def get_width(self, t: float, time: float) -> int:
        range_length = self.max_width - self.min_width
        return int(self.min_width + t * range_length)


def get_width_object(configs: ObjectConfigs | JSON_object) -> WidthABC:
    return get_object(WidthABC, configs)
