from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from coloring.color import Color
from coloring.point.ABCs import PointDrawerABC
from configs import ObjectConfigs
from utils.concrete_inheritors import get_object


@dataclass
class PlainPoint(PointDrawerABC):
    color: Color
    width: int

    @classmethod
    def from_json(
        cls,
        color: Color = (0, 0, 0),
        width: int = 1
    ) -> PlainPoint:
        return cls(color, width)

    def get_color(self, x, y):
        return self.color

    def get_width(self, x, y):
        return self.width


def get_point_object(configs: dict[str, Any] | ObjectConfigs) -> PointDrawerABC:
    return get_object(PointDrawerABC, configs)
