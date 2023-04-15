import math
from dataclasses import dataclass, field
from typing import Any, Optional

from coloring.ABCs import (GradientABC, LineColorABC, LineRangeABC,
                           PositionRangeABC)
from coloring.color import Color, ColorHSV, ColorRGB
from coloring.gradient import get_gradient_object
from coloring.line_range import get_line_range_object
from coloring.position_range import get_image_range_object
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class Plain(LineColorABC):
    color: Color

    def get_color(self, edge: Edge, t: float) -> Color:
        return self.color


@dataclass
class GradientRGB(LineColorABC):
    start_color: dict[str, Any]
    end_color: dict[str, Any]
    range: dict[str, Any] = field(default_factory=dict)
    _start_color: Optional[GradientABC[ColorRGB]] = field(init=False)
    _end_color: Optional[GradientABC[ColorRGB]] = field(init=False)
    _range: Optional[PositionRangeABC] = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = get_gradient_object(self.start_color)
        self._end_color = get_gradient_object(self.end_color)
        self._range = get_image_range_object(self.range)

    def get_color(self, edge: Edge, t: float) -> Color:
        if self._start_color is None or self._end_color is None or self._range is None:
            return (0, 0, 0)
        current_start_color = self._start_color.get_color(t)
        current_end_color = self._start_color.get_color(t)
        return ColorRGB.interpolate(
            current_start_color, current_end_color, self._range.get_value(edge.midpoint(), t)
        ).make_drawable()


@dataclass
class GradientHSV(LineColorABC):
    start_color: dict[str, Any]
    end_color: dict[str, Any]
    range: dict[str, Any]
    _start_color: Optional[GradientABC[ColorHSV]] = field(init=False)
    _end_color: Optional[GradientABC[ColorHSV]] = field(init=False)
    _range: Optional[PositionRangeABC] = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = get_gradient_object(self.start_color)
        self._end_color = get_gradient_object(self.end_color)
        self._range = get_image_range_object(self.range)

    def get_color(self, edge: Edge, t: float) -> Color:
        if self._start_color is None or self._end_color is None or self._range is None:
            return (0, 0, 0)
        current_start_color = self._start_color.get_color(t)
        current_end_color = self._end_color.get_color(t)
        return ColorHSV.interpolate(
            current_start_color, current_end_color, self._range.get_value(edge.midpoint(), t)
        ).make_drawable()


@dataclass
class LineGradientRGB(LineColorABC):
    start_color: dict[str, Any]
    end_color: dict[str, Any]
    range: dict[str, Any]
    _start_color: Optional[GradientABC[ColorRGB]] = field(init=False)
    _end_color: Optional[GradientABC[ColorRGB]] = field(init=False)
    _range: Optional[LineRangeABC] = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = get_gradient_object(self.start_color)
        self._end_color = get_gradient_object(self.end_color)
        self._range = get_line_range_object(self.range)

    def get_color(self, edge: Edge, t: float) -> Color:
        if self._start_color is None or self._end_color is None or self._range is None:
            return (0, 0, 0)
        current_start_color = self._start_color.get_color(t)
        current_end_color = self._end_color.get_color(t)
        return ColorRGB.interpolate(
            current_start_color, current_end_color, self._range.get_value(edge.midpoint(), t)
        ).make_drawable()


@dataclass
class LineGradientHSV(LineColorABC):
    start_color: dict[str, Any]
    end_color: dict[str, Any]
    range: dict[str, Any]
    _start_color: Optional[GradientABC[ColorHSV]] = field(init=False)
    _end_color: Optional[GradientABC[ColorHSV]] = field(init=False)
    _range: Optional[LineRangeABC] = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = get_gradient_object(self.start_color)
        self._end_color = get_gradient_object(self.end_color)
        self._range = get_line_range_object(self.range)

    def get_color(self, edge: Edge, t: float) -> Color:
        if self._start_color is None or self._end_color is None or self._range is None:
            return (0, 0, 0)
        current_start_color = self._start_color.get_color(t)
        current_end_color = self._end_color.get_color(t)
        return ColorHSV.interpolate(
            current_start_color, current_end_color, self._range.get_value(edge.midpoint(), t)
        ).make_drawable()


def get_line_color_object(configs: ObjectConfigs | dict[str, Any]) -> Optional[LineColorABC]:
    return get_object(LineColorABC, configs)