from __future__ import annotations

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
    color: ColorRGB

    @classmethod
    def from_json(cls, color: Color) -> PlainRGB:
        return cls(color=ColorRGB.generate(color))

    def get_color(self, t: float) -> ColorRGB:
        return self.color


@dataclass
class PlainHSV(GradientABC[ColorHSV]):
    color: ColorHSV

    @classmethod
    def from_json(cls, color: Color) -> PlainHSV:
        return cls(color=ColorHSV.generate(color))

    def get_color(self, t: float) -> ColorHSV:
        return self.color


@dataclass
class GradientRGB(GradientABC[ColorRGB]):
    start_color: ColorRGB
    end_color: ColorRGB
    range: ReflectiveRangeABC

    @classmethod
    def from_json(
        cls,
        start_color: Color,
        end_color: Color,
        range: dict[str, Any]
    ) -> GradientRGB:
        return cls(
            start_color=ColorRGB.generate(start_color),
            end_color=ColorRGB.generate(end_color),
            range=get_reflective_range_object(range)
        )

    def get_color(self, t: float) -> ColorRGB:
        t = self.range.get_value(t)
        return ColorRGB.interpolate(self.start_color, self.end_color, t)


@dataclass
class GradientHSV(GradientABC[ColorHSV]):
    start_color: ColorHSV
    end_color: ColorHSV
    range: ReflectiveRangeABC

    @classmethod
    def from_json(
        cls,
        start_color: Color,
        end_color: Color,
        range: dict[str, Any]
    ) -> GradientHSV:
        return cls(
            start_color=ColorHSV.generate(start_color),
            end_color=ColorHSV.generate(end_color),
            range=get_reflective_range_object(range)
        )

    def get_color(self, t: float) -> ColorHSV:
        t = self.range.get_value(t)
        return ColorHSV.interpolate(self.start_color, self.end_color, t)


def get_gradient_object(configs: ObjectConfigs | dict[str, Any]) -> GradientABC:
    return get_object(GradientABC, configs)
