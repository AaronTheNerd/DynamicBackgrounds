from __future__ import annotations

from dataclasses import dataclass

from coloring.color import Color
from utils.serialABC import SerialABC


@dataclass
class PointDrawer(SerialABC):
    color: Color
    width: int

    @classmethod
    def from_json(
        cls,
        color: Color = (0, 0, 0),
        width: int = 1
    ) -> PointDrawer:
        return cls(color, width)

    def get_color(self, x, y):
        return self.color

    def get_width(self, x, y):
        return self.width
