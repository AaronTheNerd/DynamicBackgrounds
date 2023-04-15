from dataclasses import dataclass
from typing import Any, Optional

from coloring.ABCs import PointColorerABC
from coloring.color import Color
from configs import ObjectConfigs
from utils.concrete_inheritors import get_object


@dataclass
class PlainPoint(PointColorerABC):
    color: Color = (0, 0, 0)
    width: int = 1

    def get_color(self, x, y):
        return self.color

    def get_width(self, x, y):
        return self.width


def get_point_object(configs: dict[str, Any] | ObjectConfigs) -> Optional[PointColorerABC]:
    return get_object(PointColorerABC, configs)
