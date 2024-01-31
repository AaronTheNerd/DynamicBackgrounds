from __future__ import annotations

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
    color: ColorABC
    width: WidthABC

    @classmethod
    def from_json(
        cls,
        color: dict[str, Any],
        width: dict[str, Any]
    ) -> LineDrawer:
        return cls(
            color=get_line_color_object(color),
            width=get_line_width_object(width)
        )

    def get_color(self, edge: Edge, t: float) -> Color:
        return self.color.get_color(edge, t)

    def get_width(self, edge: Edge, t: float) -> int:
        return self.width.get_width(edge, t)


def get_line_object(configs: dict[str, Any] | ObjectConfigs) -> LineDrawerABC:
    return get_object(LineDrawerABC, configs)
