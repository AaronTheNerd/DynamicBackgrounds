from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from coloring.ABCs import GradientABC
from coloring.color import Color, ColorHSV, ColorRGB
from coloring.gradient import get_gradient_object
from coloring.line.ABCs import ColorABC
from coloring.range.ABCs import LineRangeABC, PositionRangeABC
from coloring.range.line_range import get_line_range_object
from coloring.range.position_range import get_image_range_object
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class Plain(ColorABC):
    color: Color

    @classmethod
    def from_json(cls, color: Color) -> Plain:
        return cls(color)

    def get_color(self, edge: Edge, t: float) -> Color:
        return self.color


@dataclass
class GradientRGB(ColorABC):
    start_color: GradientABC[ColorRGB]
    end_color: GradientABC[ColorRGB]
    range: PositionRangeABC

    @classmethod
    def from_json(
        cls,
        start_color: dict[str, Any],
        end_color: dict[str, Any],
        range: dict[str, Any]
    ) -> GradientRGB:
        return cls(
            start_color=get_gradient_object(start_color),
            end_color=get_gradient_object(end_color),
            range=get_image_range_object(range)
        )

    def get_color(self, edge: Edge, t: float) -> Color:
        current_start_color = self.start_color.get_color(t)
        current_end_color = self.start_color.get_color(t)
        return ColorRGB.interpolate(
            current_start_color, current_end_color, self.range.get_value(edge.midpoint(), t)
        ).make_drawable()


@dataclass
class GradientHSV(ColorABC):
    start_color: GradientABC[ColorHSV]
    end_color: GradientABC[ColorHSV]
    range: PositionRangeABC

    @classmethod
    def from_json(
        cls,
        start_color: dict[str, Any],
        end_color: dict[str, Any],
        range: dict[str, Any]
    ) -> GradientHSV:
        return cls(
            start_color=get_gradient_object(start_color),
            end_color=get_gradient_object(end_color),
            range=get_image_range_object(range)
        )

    def get_color(self, edge: Edge, t: float) -> Color:
        current_start_color = self.start_color.get_color(t)
        current_end_color = self.end_color.get_color(t)
        return ColorHSV.interpolate(
            current_start_color, current_end_color, self.range.get_value(edge.midpoint(), t)
        ).make_drawable()


@dataclass
class LineGradientRGB(ColorABC):
    start_color: GradientABC[ColorRGB]
    end_color: GradientABC[ColorRGB]
    range: LineRangeABC

    @classmethod
    def from_json(
        cls,
        start_color: dict[str, Any],
        end_color: dict[str, Any],
        range: dict[str, Any]
    ) -> GradientHSV:
        return cls(
            start_color=get_gradient_object(start_color),
            end_color=get_gradient_object(end_color),
            range=get_line_range_object(range)
        )

    def get_color(self, edge: Edge, t: float) -> Color:
        current_start_color = self.start_color.get_color(t)
        current_end_color = self.end_color.get_color(t)
        return ColorRGB.interpolate(
            current_start_color, current_end_color, self.range.get_value(edge, t)
        ).make_drawable()


@dataclass
class LineGradientHSV(ColorABC):
    start_color: GradientABC[ColorHSV]
    end_color: GradientABC[ColorHSV]
    range: LineRangeABC

    @classmethod
    def from_json(
        cls,
        start_color: dict[str, Any],
        end_color: dict[str, Any],
        range: dict[str, Any]
    ) -> LineGradientHSV:
        return cls(
            start_color=get_gradient_object(start_color),
            end_color=get_gradient_object(end_color),
            range=get_line_range_object(range)
        )

    def get_color(self, edge: Edge, t: float) -> Color:
        current_start_color = self.start_color.get_color(t)
        current_end_color = self.end_color.get_color(t)
        return ColorHSV.interpolate(
            current_start_color, current_end_color, self.range.get_value(edge, t)
        ).make_drawable()


def get_line_color_object(configs: ObjectConfigs | dict[str, Any]) -> ColorABC:
    return get_object(ColorABC, configs)
