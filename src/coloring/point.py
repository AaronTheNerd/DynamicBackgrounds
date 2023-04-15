from dataclasses import dataclass
from typing import Any, Dict, Optional

from coloring.ABCs import PointColorABC
from coloring.color import Color
from configs import ObjectConfigs
from utils.concrete_inheritors import get_object


@dataclass
class PlainPoint(PointColorABC):
    color: Color = (0, 0, 0)
    width: int = 1

    def get_color(self, x, y):
        return self.color

    def get_width(self, x, y):
        return self.width


def get_point_object(configs: Dict[str, Any] | ObjectConfigs) -> Optional[PointColorABC]:
    return get_object(PointColorABC, configs)
