from dataclasses import dataclass, field
from typing import Any

from coloring.ABCs import LineColorABC, LineColorerABC, LineWidthABC
from coloring.color import Color
from coloring.line_color import get_line_color_object
from coloring.line_width import get_line_width_object
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class LineColorer(LineColorerABC):
    color: dict[str, Any]
    width: dict[str, Any]
    _color: LineColorABC = field(init=False)
    _width: LineWidthABC = field(init=False)

    def __post_init__(self) -> None:
        self._color = get_line_color_object(self.color)
        self._width = get_line_width_object(self.width)

    def get_color(self, edge: Edge, t: float) -> Color:
        return self._color.get_color(edge, t)

    def get_width(self, edge: Edge, t: float) -> int:
        return self._width.get_width(edge, t)


def get_line_object(configs: dict[str, Any] | ObjectConfigs) -> LineColorerABC:
    return get_object(LineColorerABC, configs)
