from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from coloring.color import Color, ColorRGB
from coloring.triangle.ABCs import ColorABC, ShaderABC, TriangleDrawerABC
from coloring.triangle.color import get_triangle_color_object
from coloring.triangle.shader import get_shader_object
from configs import ObjectConfigs
from triangle import Triangle
from utils.concrete_inheritors import get_object


@dataclass
class TriangleDrawer(TriangleDrawerABC):
    gradient: Optional[ColorABC] = None
    shader: Optional[ShaderABC] = None

    @classmethod
    def from_json(
        cls,
        gradient: Optional[dict[str, Any]] = None,
        shader: Optional[dict[str, Any]] = None
    ) -> TriangleDrawer:
        real_gradient = None
        if gradient is not None:
            real_gradient = get_triangle_color_object(gradient)
        real_shader = None
        if shader is not None:
            real_shader = get_shader_object(shader)
        return cls(real_gradient, real_shader)

    def get_color(self, triangle: Triangle, t: float) -> Color:
        color = (255, 255, 255)
        if self.gradient is not None:
            color = self.gradient.get_color(triangle, t)
        facing_ratio = 1.0
        if self.shader is not None:
            facing_ratio = self.shader.get_facing_ratio(triangle, t)
        return ColorRGB.interpolate(
            ColorRGB(0, 0, 0), ColorRGB.generate(color), facing_ratio
        ).make_drawable()


def get_triangle_object(configs: dict[str, Any] | ObjectConfigs) -> TriangleDrawerABC:
    return get_object(TriangleDrawerABC, configs)
