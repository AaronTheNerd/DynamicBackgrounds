from dataclasses import dataclass, field
from typing import Any

from coloring.color import Color
from coloring.line.ABCs import ColorABC, LineDrawerABC, WidthABC
from coloring.line.color import get_line_color_object
from coloring.line.width import get_line_width_object
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class LineDrawer(LineDrawerABC):
    color: dict[str, Any]
    width: dict[str, Any]
    _color: ColorABC = field(init=False)
    _width: WidthABC = field(init=False)

    def __post_init__(self) -> None:
        self._color = get_line_color_object(self.color)
        self._width = get_line_width_object(self.width)

    def get_color(self, edge: Edge, t: float) -> Color:
        return self._color.get_color(edge, t)

    def get_width(self, edge: Edge, t: float) -> int:
        return self._width.get_width(edge, t)


def get_line_object(configs: dict[str, Any] | ObjectConfigs) -> LineDrawerABC:
    return get_object(LineDrawerABC, configs)
