from __future__ import annotations

from dataclasses import dataclass

from color import Color
from serial.ABCs import SerialABC


@dataclass
class VertexDrawer(SerialABC):
    color: Color
    width: int

    @classmethod
    def from_json(cls, color: Color = (0, 0, 0), width: int = 1) -> VertexDrawer:
        return cls(color, width)

    def get_color(self, x, y):
        return self.color

    def get_width(self, x, y):
        return self.width
