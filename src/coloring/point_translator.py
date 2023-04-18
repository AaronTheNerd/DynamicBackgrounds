import math
from dataclasses import dataclass, field
from typing import Any

from coloring.ABCs import PointTranslatorABC
from configs import ObjectConfigs
from point.point import Static as StaticPoint
from utils.concrete_inheritors import get_object


@dataclass
class Static(PointTranslatorABC):
    point: list[float]
    _point: StaticPoint = field(init=False)

    def __post_init__(self) -> None:
        self._point = StaticPoint(self.point[0], self.point[1], 0)

    def get_point(self, t: float) -> StaticPoint:
        return self._point


@dataclass
class Circle(PointTranslatorABC):
    start: list[float]
    center: list[float]
    CW: bool = True
    _start: StaticPoint = field(init=False)
    _center: StaticPoint = field(init=False)

    def __post_init__(self) -> None:
        self._start = StaticPoint(self.start[0], self.start[1], 0)
        self._center = StaticPoint(self.center[0], self.center[1], 0)

    def get_point(self, t: float) -> StaticPoint:
        rad = t * 2 * math.pi
        if not self.CW:
            rad = -rad
        point = StaticPoint(self._start.x - self._center.x, self._start.y - self._center.y, 0)
        point = StaticPoint(
            point.x * math.cos(rad) - point.y * math.sin(rad),
            point.y * math.cos(rad) + point.x * math.sin(rad),
            0,
        )
        point.x += self._center.x
        point.y += self._center.y
        return point


def get_point_translator_object(configs: ObjectConfigs | dict[str, Any]) -> PointTranslatorABC:
    return get_object(PointTranslatorABC, configs)
