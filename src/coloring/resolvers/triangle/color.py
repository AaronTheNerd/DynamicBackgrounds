from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from color import Color
from coloring.gradient.ABCs import GradientABC
from coloring.gradient.gradient import get_gradient_object
from coloring.metric.ABCs import TriangleMetricABC
from coloring.metric.metric import get_metric_object
from coloring.metric_modifier.ABCs import ModifierABC
from coloring.metric_modifier.modifier import get_metric_modifier_object
from coloring.misc_triangle_color.ABCs import MiscTriangleColorABC
from coloring.misc_triangle_color.color import get_misc_triangle_color_object
from coloring.resolvers.triangle.ABCs import TriangleColorResolverABC
from coloring.shader.ABCs import ShaderABC
from coloring.shader.shader import get_shader_object
from configs import ObjectConfigs
from serial.JSON_types import JSON_object
from triangle.triangle import Triangle
from utils.concrete_inheritors import get_object


@dataclass
class TriangleGradient(TriangleColorResolverABC):
    gradient: GradientABC
    metric: Optional[TriangleMetricABC]
    metric_modifiers: list[ModifierABC]
    shader: Optional[ShaderABC]

    @classmethod
    def from_json(
        cls,
        gradient: JSON_object,
        metric: Optional[JSON_object] = None,
        metric_modifiers: Optional[list[JSON_object]] = None,
        shader: Optional[JSON_object] = None,
    ) -> TriangleGradient:
        parsed_metric = None
        if metric is not None:
            parsed_metric = get_metric_object(metric)
        if metric_modifiers is None:
            metric_modifiers = []
        parsed_shader = None
        if shader is not None:
            parsed_shader = get_shader_object(shader)
        return cls(
            gradient=get_gradient_object(gradient),
            metric=parsed_metric,
            metric_modifiers=[
                get_metric_modifier_object(metric_modifier)
                for metric_modifier in metric_modifiers
            ],
            shader=parsed_shader,
        )

    def get_color(self, triangle: Triangle, time: float) -> Color:
        t = 0
        if self.metric is not None:
            t = self.metric.measure_triangle(triangle, time)
        for modifier in self.metric_modifiers:
            t = modifier.get_value(t)
        unshaded_color = self.gradient.get_color(t, time)
        shading_ratio = 1.0
        if self.shader is not None:
            shading_ratio = self.shader.get_facing_ratio(triangle, time)
        return Color.interpolateRGB(Color(0, 0, 0), unshaded_color, shading_ratio)


@dataclass
class MiscTriangleColor(TriangleColorResolverABC):
    color: MiscTriangleColorABC

    @classmethod
    def from_json(cls, color: JSON_object) -> MiscTriangleColor:
        return cls(get_misc_triangle_color_object(color))

    def get_color(self, triangle: Triangle, time: float) -> Color:
        return self.color.get_color(triangle, time)


def get_triangle_color_resolver_object(
    configs: ObjectConfigs | JSON_object,
) -> TriangleColorResolverABC:
    return get_object(TriangleColorResolverABC, configs)
