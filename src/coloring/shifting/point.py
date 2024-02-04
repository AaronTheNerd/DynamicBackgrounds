from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from coloring.shifting.ABCs import ShiftingPointABC
from configs import ObjectConfigs
from point.point import Static as StaticPoint
from serial.JSON_types import JSON_point
from utils.concrete_inheritors import get_object


@dataclass
class Static(ShiftingPointABC):
    point: StaticPoint

    @classmethod
    def from_json(cls, point: JSON_point) -> Static:
        return cls(point=StaticPoint(*point))

    def get_point(self, t: float) -> StaticPoint:
        return self.point


@dataclass
class Circle(ShiftingPointABC):
    start: StaticPoint
    center: StaticPoint
    CW: bool = True

    @classmethod
    def from_json(cls, start: list[float], center: list[float], CW: bool) -> Circle:
        return cls(start=StaticPoint(*start), center=StaticPoint(*center), CW=CW)

    def get_point(self, t: float) -> StaticPoint:
        rad = t * 2 * math.pi
        if not self.CW:
            rad = -rad
        point = StaticPoint(
            self.start.x - self.center.x, self.start.y - self.center.y, 0
        )
        point = StaticPoint(
            point.x * math.cos(rad) - point.y * math.sin(rad),
            point.y * math.cos(rad) + point.x * math.sin(rad),
            0,
        )
        point.x += self.center.x
        point.y += self.center.y
        return point


def get_shifting_point_object(
    configs: ObjectConfigs | dict[str, Any]
) -> ShiftingPointABC:
    return get_object(ShiftingPointABC, configs)
