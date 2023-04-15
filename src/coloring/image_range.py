from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from coloring.ABCs import ImageRangeABC, RangeABC
from configs import CONFIGS, ObjectConfigs
from triangle import Triangle
from coloring.range import get_range_object
from utils.concrete_inheritors import get_object


@dataclass
class Distance(ImageRangeABC):
    start_x: int = 0
    start_y: int = 0
    end_x: int = CONFIGS.gif_configs.width
    end_y: int = CONFIGS.gif_configs.height
    range: Dict[str, Any] = field(default_factory=dict)
    _dx: float = field(init=False)
    _dy: float = field(init=False)
    _range: Optional[RangeABC] = field(init=False)

    def __post_init__(self) -> None:
        self._dx = self.end_x - self.start_x
        self._dy = self.end_y - self.start_y
        self._range = get_range_object(self.range)

    def get_value(self, triangle: Triangle, t: float) -> float:
        center = triangle.center()
        x, y = center.x, center.y
        t = (self._dx * (x - self.start_x) + self._dy * (y - self.start_y)) / (
            (self._dx) ** 2 + (self._dy) ** 2
        )
        t = max(0.0, min(t, 1.0))
        if self._range is not None:
            t = self._range.get_value(t)
        return t


def get_image_range_object(configs: Dict[str, Any] | ObjectConfigs) -> Optional[ImageRangeABC]:
    return get_object(ImageRangeABC, configs)
