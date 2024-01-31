from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from coloring.ABCs import PointTranslatorABC
from coloring.point_translator import get_point_translator_object
from coloring.range.ABCs import PositionRangeABC, RangeABC
from coloring.range.range import get_range_object
from configs import ObjectConfigs
from point.ABCs import PointABC
from utils.concrete_inheritors import get_object


@dataclass
class Linear(PositionRangeABC):
    start: PointTranslatorABC
    end: PointTranslatorABC
    range: RangeABC

    @classmethod
    def from_json(
        cls,
        start: dict[str, Any],
        end: dict[str, Any],
        range: dict[str, Any]
    ) -> Linear:
        return cls(
            start=get_point_translator_object(start),
            end=get_point_translator_object(end),
            range=get_range_object(range)
        )

    def get_value(self, point: PointABC, t: float) -> float:
        current_start = self.start.get_point(t)
        current_end = self.end.get_point(t)
        dx = current_end.x - current_start.x
        dy = current_end.y - current_start.y
        t = (dx * (point.x - current_start.x) + dy * (point.y - current_start.y)) / (
            math.pow(dx, 2) + math.pow(dy, 2)
        )
        t = max(0.0, min(t, 1.0))
        t = self.range.get_value(t)
        return t


@dataclass
class Radial(PositionRangeABC):
    min_radius: float
    max_radius: float
    center: PointTranslatorABC
    range: RangeABC

    @classmethod
    def from_json(
        cls,
        min_radius: float,
        max_radius: float,
        center: dict[str, Any],
        range: dict[str, Any]
    ) -> Radial:
        return cls(
            min_radius=min_radius,
            max_radius=max_radius,
            center=get_point_translator_object(center),
            range=get_range_object(range)
        )

    def get_value(self, point: PointABC, t: float) -> float:
        current_center = self.center.get_point(t)
        dist = math.sqrt(
            math.pow(point.x - current_center.x, 2) + math.pow(point.y - current_center.y, 2)
        )
        t = (dist - self.min_radius) / (self.max_radius - self.min_radius)
        t = max(0.0, min(t, 1.0))
        t = self.range.get_value(t)
        return t


def get_image_range_object(configs: dict[str, Any] | ObjectConfigs) -> PositionRangeABC:
    return get_object(PositionRangeABC, configs)
