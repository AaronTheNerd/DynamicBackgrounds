from __future__ import annotations

from dataclasses import dataclass

from color import Color
from coloring.metric_modifier.ABCs import ReflectiveModifierABC
from coloring.metric_modifier.modifier import get_reflective_metric_modifier_object
from coloring.shifting.ABCs import ShiftingColorABC
from configs import ObjectConfigs
from serial.JSON_types import JSON_color, JSON_object
from utils.concrete_inheritors import get_object


@dataclass
class Static(ShiftingColorABC):
    color: Color

    @classmethod
    def from_json(cls, color: JSON_color) -> Static:
        return cls(color=Color.from_json(color))

    def get_color(self, time: float) -> Color:
        return self.color


@dataclass
class Gradient(ShiftingColorABC):
    start_color: Color
    end_color: Color
    hsv: bool
    reflection: ReflectiveModifierABC

    @classmethod
    def from_json(
        cls,
        start_color: JSON_color,
        end_color: JSON_color,
        reflection: JSON_object,
        interpolator: str = "RGB",
    ) -> Gradient:
        hsv = interpolator == "HSV"
        return cls(
            start_color=Color.from_json(start_color),
            end_color=Color.from_json(end_color),
            hsv=hsv,
            reflection=get_reflective_metric_modifier_object(reflection),
        )

    def get_color(self, time: float) -> Color:
        t = self.reflection.get_value(time)
        if self.hsv:
            return Color.interpolateHSV(self.start_color, self.end_color, t)
        return Color.interpolateRGB(self.start_color, self.end_color, t)


def get_shifting_color_object(configs: ObjectConfigs | JSON_object) -> ShiftingColorABC:
    return get_object(ShiftingColorABC, configs)
