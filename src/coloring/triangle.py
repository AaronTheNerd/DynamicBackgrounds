from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from color import Color, image_color
from coloring.resolvers.triangle_color import TriangleColorResolver
from serial.JSON_types import JSON_object
from triangle import Triangle
from serial.ABCs import SerialABC

@dataclass
class TriangleDrawer(SerialABC):
    color: TriangleColorResolver

    @classmethod
    def from_json(
        cls,
        color: JSON_object
    ) -> TriangleDrawer:
        return cls(
            color=TriangleColorResolver.from_json(**color)
        )

    def get_color(self, triangle: Triangle, time: float) -> image_color:
        return self.color.get_color(triangle, time).image_color()
