from __future__ import annotations

from colorsys import hsv_to_rgb, rgb_to_hsv
from dataclasses import dataclass

from utils.interpolate import interpolate
from serial.ABCs import SerialABC
from serial.JSON_types import JSON_color

image_color = tuple[int, int, int]

@dataclass
class Color(SerialABC):
    r: float
    g: float
    b: float

    @classmethod
    def from_json(cls, color: JSON_color) -> Color:
        return cls(
            color[0] / 255,
            color[1] / 255,
            color[2] / 255
        )
    
    def image_color(self) -> image_color:
        return (
            int(self.r * 255),
            int(self.g * 255),
            int(self.b * 255)
        )
    
    @classmethod
    def interpolateRGB(cls, color1: Color, color2: Color, t: float) -> Color:
        return cls(
            interpolate(color1.r, color2.r, t),
            interpolate(color1.g, color2.g, t),
            interpolate(color1.b, color2.b, t),
        )

    @classmethod
    def interpolateHSV(cls, color1: Color, color2: Color, t: float) -> Color:
        hsv_color1 = rgb_to_hsv(color1.r, color1.g, color1.b)
        hsv_color2 = rgb_to_hsv(color2.r, color2.g, color2.b)
        interpolated_hsv = [
            interpolate(c1, c2, t) for c1, c2 in zip(hsv_color1, hsv_color2)
        ]
        return cls(
            *hsv_to_rgb(*interpolated_hsv)
        )
