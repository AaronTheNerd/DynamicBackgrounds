from __future__ import annotations

from dataclasses import dataclass

from color import image_color
from coloring.resolvers.edge_color import EdgeColorResolver
from coloring.resolvers.edge_width import EdgeWidthResolver
from serial.ABCs import SerialABC
from serial.JSON_types import JSON_object
from triangle.triangle import Edge


@dataclass
class EdgeDrawer(SerialABC):
    color: EdgeColorResolver
    width: EdgeWidthResolver

    @classmethod
    def from_json(
        cls,
        color: JSON_object,
        width: JSON_object,
    ) -> EdgeDrawer:
        return cls(
            color=EdgeColorResolver.from_json(**color),
            width=EdgeWidthResolver.from_json(**width),
        )

    def get_color(self, edge: Edge, time: float) -> image_color:
        return self.color.get_color(edge, time).image_color()

    def get_width(self, edge: Edge, time: float) -> int:
        return self.width.get_width(edge, time)
