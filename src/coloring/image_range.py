import math
from dataclasses import dataclass, field
from typing import Any, Optional

from coloring.ABCs import ImageRangeABC, RangeABC, PointTranslatorABC
from configs import CONFIGS, ObjectConfigs
from point import StaticPoint
from triangle import Triangle
from coloring.range import get_range_object
from coloring.point_translator import get_point_translator_object
from utils.concrete_inheritors import get_object


@dataclass
class Linear(ImageRangeABC):
    start: dict[str, Any]
    end: dict[str, Any]
    range: dict[str, Any] = field(default_factory=dict)
    _start: Optional[PointTranslatorABC] = field(init=False)
    _end: Optional[PointTranslatorABC] = field(init=False)
    _range: Optional[RangeABC] = field(init=False)

    def __post_init__(self) -> None:
        self._start = get_point_translator_object(self.start)
        self._end = get_point_translator_object(self.end)
        self._range = get_range_object(self.range)

    def get_value(self, triangle: Triangle, t: float) -> float:
        if self._start is None or self._end is None:
            return 0.0
        center = triangle.center()
        x, y = center.x, center.y
        current_start = self._start.get_point(t)
        current_end = self._end.get_point(t)
        dx = current_end.x - current_start.x
        dy = current_end.y - current_start.y
        t = (dx * (x - current_start.x) + dy * (y - current_start.y)) / (
            math.pow(dx, 2) + math.pow(dy, 2)
        )
        t = max(0.0, min(t, 1.0))
        if self._range is not None:
            t = self._range.get_value(t)
        return t
    

@dataclass
class Radial(ImageRangeABC):
    min_radius: float
    max_radius: float
    center: dict[str, Any]
    range: dict[str, Any] = field(default_factory=dict)
    _center: Optional[PointTranslatorABC] = field(init=False)
    _range: Optional[RangeABC] = field(init=False)

    def __post_init__(self) -> None:
        self._center = get_point_translator_object(self.center)
        self._range = get_range_object(self.range)

    def get_value(self, triangle: Triangle, t: float) -> float:
        if self._center is None:
            current_center = StaticPoint(CONFIGS.full_width / 2, CONFIGS.full_height / 2)
        else:
            current_center = self._center.get_point(t)
        center = triangle.center()
        x, y = center.x, center.y
        dist = math.sqrt(math.pow(x - current_center.x, 2) + math.pow(y - current_center.y, 2))
        t = (dist - self.min_radius) / (self.max_radius - self.min_radius)
        t = max(0.0, min(t, 1.0))
        if self._range is not None:
            t = self._range.get_value(t)
        return t


def get_image_range_object(configs: dict[str, Any] | ObjectConfigs) -> Optional[ImageRangeABC]:
    return get_object(ImageRangeABC, configs)
