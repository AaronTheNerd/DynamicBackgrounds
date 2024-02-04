from __future__ import annotations

from dataclasses import dataclass

from color import Color
from coloring.gradient.ABCs import GradientABC
from coloring.shifting.ABCs import ShiftingColorABC
from coloring.shifting.color import get_shifting_color_object
from configs import ObjectConfigs
from serial.JSON_types import JSON_color, JSON_object
from utils.concrete_inheritors import get_object


@dataclass
class Plain(GradientABC):
    color: ShiftingColorABC

    @classmethod
    def from_json(cls, color: JSON_object) -> Plain:
        return cls(get_shifting_color_object(color))

    def get_color(self, t: float, time: float) -> Color:
        return self.color.get_color(time)


@dataclass
class Gradient(GradientABC):
    start_color: ShiftingColorABC
    end_color: ShiftingColorABC
    hsv: bool

    @classmethod
    def from_json(
        cls, start_color: JSON_object, end_color: JSON_object, interpolator: str = "RGB"
    ) -> Gradient:
        hsv = interpolator == "HSV"
        return cls(
            start_color=get_shifting_color_object(start_color),
            end_color=get_shifting_color_object(end_color),
            hsv=hsv,
        )

    def get_color(self, t: float, time: float) -> Color:
        current_start_color = self.start_color.get_color(time)
        current_end_color = self.end_color.get_color(time)
        if self.hsv:
            return Color.interpolateHSV(current_start_color, current_end_color, t)
        return Color.interpolateRGB(current_start_color, current_end_color, t)


def get_gradient_object(configs: ObjectConfigs | JSON_object) -> GradientABC:
    return get_object(GradientABC, configs)
