from dataclasses import dataclass, field
from typing import Any

from coloring.ABCs import GradientABC
from coloring.color import Color, ColorHSV, ColorRGB
from coloring.range.ABCs import ReflectiveRangeABC
from coloring.range.reflective_range import get_reflective_range_object
from configs import ObjectConfigs
from utils.concrete_inheritors import get_object


@dataclass
class PlainRGB(GradientABC[ColorRGB]):
    color: Color
    _color: ColorRGB = field(init=False)

    def __post_init__(self) -> None:
        self._color = ColorRGB.generate(self.color)

    def get_color(self, t: float) -> ColorRGB:
        return self._color


@dataclass
class PlainHSV(GradientABC[ColorHSV]):
    color: Color
    _color: ColorHSV = field(init=False)

    def __post_init__(self) -> None:
        self._color = ColorHSV.generate(self.color)

    def get_color(self, t: float) -> ColorHSV:
        return self._color


@dataclass
class GradientRGB(GradientABC[ColorRGB]):
    start_color: Color
    end_color: Color
    range: dict[str, Any]
    _start_color: ColorRGB = field(init=False)
    _end_color: ColorRGB = field(init=False)
    _range: ReflectiveRangeABC = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = ColorRGB.generate(self.start_color)
        self._end_color = ColorRGB.generate(self.end_color)
        self._range = get_reflective_range_object(self.range)

    def get_color(self, t: float) -> ColorRGB:
        t = self._range.get_value(t)
        return ColorRGB.interpolate(self._start_color, self._end_color, t)


@dataclass
class GradientHSV(GradientABC[ColorHSV]):
    start_color: Color
    end_color: Color
    range: dict[str, Any]
    _start_color: ColorHSV = field(init=False)
    _end_color: ColorHSV = field(init=False)
    _range: ReflectiveRangeABC = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = ColorHSV.generate(self.start_color)
        self._end_color = ColorHSV.generate(self.end_color)
        self._range = get_reflective_range_object(self.range)

    def get_color(self, t: float) -> ColorHSV:
        t = self._range.get_value(t)
        return ColorHSV.interpolate(self._start_color, self._end_color, t)


def get_gradient_object(configs: ObjectConfigs | dict[str, Any]) -> GradientABC:
    return get_object(GradientABC, configs)
