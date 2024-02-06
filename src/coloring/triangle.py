from __future__ import annotations

from dataclasses import dataclass

from color import image_color
from coloring.resolvers.triangle.ABCs import TriangleColorResolverABC
from coloring.resolvers.triangle.color import get_triangle_color_resolver_object
from serial.ABCs import SerialABC
from serial.JSON_types import JSON_object
from triangle import Triangle


@dataclass
class TriangleDrawer(SerialABC):
    color: TriangleColorResolverABC

    @classmethod
    def from_json(cls, color: JSON_object) -> TriangleDrawer:
        return cls(color=get_triangle_color_resolver_object(color))

    def get_color(self, triangle: Triangle, time: float) -> image_color:
        return self.color.get_color(triangle, time).image_color()

