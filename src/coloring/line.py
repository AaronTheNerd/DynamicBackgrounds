import math
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from coloring.ABCs import LineColorABC
from coloring.color import Color, ColorHSV, ColorRGB
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class SolidLine(LineColorABC):
    color: Color = (0, 0, 0)
    width: int = 1

    def get_color(self, edge: Edge) -> Color:
        return self.color

    def get_width(self, edge: Edge) -> int:
        return self.width


@dataclass
class FadingLineRGB(LineColorABC):
    start_color: Color = (1, 1, 1)
    end_color: Color = (0, 0, 0)
    min_dist: float = 0.0
    max_dist: float = 0.0
    width: int = 1
    _start_color: ColorRGB = field(init=False)
    _end_color: ColorRGB = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = ColorRGB.generate(self.start_color)
        self._end_color = ColorRGB.generate(self.end_color)

    def get_color_at(self, t: float) -> Color:
        return ColorRGB.interpolate(self._start_color, self._end_color, t).make_drawable()

    def get_color(self, edge: Edge) -> Color:
        dist = math.sqrt((edge[0].x - edge[1].x) ** 2 + (edge[0].y - edge[1].y) ** 2)
        if dist < self.min_dist:
            return self.start_color
        if dist > self.max_dist:
            return self.end_color
        t = (dist - self.min_dist) / (self.max_dist - self.min_dist)
        return self.get_color_at(t)

    def get_width(self, edge: Edge) -> int:
        return self.width


@dataclass
class FadingLine(LineColorABC):
    start_color: Color = (0, 0, 0)
    end_color: Color = (255, 255, 255)
    min_dist: int = 0
    max_dist: int = 0
    width: int = 1
    _start_color: ColorHSV = field(init=False)
    _end_color: ColorHSV = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = ColorHSV.generate(self.start_color)
        self._end_color = ColorHSV.generate(self.end_color)

    def get_color_at(self, t: float) -> Color:
        return ColorHSV.interpolate(self._start_color, self._end_color, t).make_drawable()

    def get_color(self, edge: Edge) -> Color:
        dist = math.sqrt((edge[0].x - edge[1].x) ** 2 + (edge[0].y - edge[1].y) ** 2)
        if dist < self.min_dist:
            return self.start_color
        if dist > self.max_dist:
            return self.end_color
        t = (dist - self.min_dist) / (self.max_dist - self.min_dist)
        return self.get_color_at(t)

    def get_width(self, edge: Edge) -> int:
        return self.width


def get_line_object(configs: Dict[str, Any] | ObjectConfigs) -> Optional[LineColorABC]:
    return get_object(LineColorABC, configs)
