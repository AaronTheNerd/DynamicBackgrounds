import math
from dataclasses import dataclass, field
from typing import Any, Optional

from coloring.ABCs import PointTranslatorABC
from configs import CONFIGS, ObjectConfigs
from point import StaticPoint
from utils.concrete_inheritors import get_object


@dataclass
class Static(PointTranslatorABC):
    point: Optional[list[float]] = None
    _point: StaticPoint = field(init=False)
    
    def __post_init__(self) -> None:
        if self.point is None:
            self._point = StaticPoint(CONFIGS.full_width / 2, CONFIGS.full_height / 2)
        else:
            self._point = StaticPoint(self.point[0], self.point[1])

    def get_point(self, t: float) -> StaticPoint:
        return self._point
    

@dataclass
class Circle(PointTranslatorABC):
    start: list[float]
    center: Optional[list[float]] = None
    CW: bool = True
    _start: StaticPoint = field(init=False)
    _center: StaticPoint = field(init=False)

    def __post_init__(self) -> None:
        self._start = StaticPoint(self.start[0], self.start[1])
        if self.center is None:
            self._center = StaticPoint(CONFIGS.full_width / 2, CONFIGS.full_height / 2)
        else:
            self._center = StaticPoint(self.center[0], self.center[1])


    def get_point(self, t: float) -> StaticPoint:
        rad = t * 2 * math.pi
        if not self.CW:
            rad = -rad
        point = StaticPoint(self._start.x - self._center.x, self._start.y - self._center.y)
        point = StaticPoint(
            point.x * math.cos(rad) - point.y * math.sin(rad),
            point.y * math.cos(rad) + point.x * math.sin(rad))
        point.x += self._center.x
        point.y += self._center.y
        return point


def get_point_translator_object(configs: ObjectConfigs | dict[str, Any]) -> Optional[PointTranslatorABC]:
    return get_object(PointTranslatorABC, configs)