import math
from dataclasses import dataclass, field
from typing import Any, Optional

from coloring.ABCs import LineColorerABC, LineColorABC, LineWidthABC
from coloring.color import Color, ColorHSV, ColorRGB
from coloring.line_color import get_line_color_object
from coloring.line_width import get_line_width_object
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class LineColorer(LineColorerABC):
    color: dict[str, Any]
    width: dict[str, Any]
    _color: Optional[LineColorABC] = field(init=False)
    _width: Optional[LineWidthABC] = field(init=False)

    def __post_init__(self) -> None:
        self._color = get_line_color_object(self.color)
        self._width = get_line_width_object(self.width)

    def get_color(self, edge: Edge, t: float) -> Color:
        if self._color is None:
            return (0, 0, 0)
        return self._color.get_color(edge, t)

    def get_width(self, edge: Edge, t: float) -> int:
        if self._width is None:
            return 0
        return self._width.get_width(edge, t)


def get_line_object(configs: dict[str, Any] | ObjectConfigs) -> Optional[LineColorerABC]:
    return get_object(LineColorerABC, configs)
