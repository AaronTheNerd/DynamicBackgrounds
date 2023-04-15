from __future__ import annotations

from colorsys import hsv_to_rgb, rgb_to_hsv
from dataclasses import dataclass

from utils.interpolate import interpolate

Color = tuple[int, int, int]


@dataclass
class ColorRGB:
    r: int
    g: int
    b: int

    @classmethod
    def generate(cls, color: Color) -> ColorRGB:
        return cls(*color)

    @classmethod
    def convert(cls, color: ColorHSV) -> ColorRGB:
        return cls(*[int(255 * i) for i in hsv_to_rgb(color.h, color.s, color.v)])

    @classmethod
    def interpolate(cls, c1: ColorRGB, c2: ColorRGB, t: float) -> ColorRGB:
        return cls(
            int(interpolate(c1.r, c2.r, t)),
            int(interpolate(c1.g, c2.g, t)),
            int(interpolate(c1.b, c2.b, t)),
        )

    def make_drawable(self) -> Color:
        return (self.r, self.g, self.b)


@dataclass
class ColorHSV:
    h: float
    s: float
    v: float

    @classmethod
    def generate(cls, color: Color) -> ColorHSV:
        return cls.convert(ColorRGB.generate(color))

    @classmethod
    def convert(cls, color: ColorRGB) -> ColorHSV:
        return cls(*rgb_to_hsv(color.r / 255, color.g / 255, color.b / 255))

    @classmethod
    def interpolate(cls, c1: ColorHSV, c2: ColorHSV, t: float) -> ColorHSV:
        return cls(
            interpolate(c1.h, c2.h, t), interpolate(c1.s, c2.s, t), interpolate(c1.v, c2.v, t)
        )

    def make_drawable(self) -> Color:
        return ColorRGB.convert(self).make_drawable()
