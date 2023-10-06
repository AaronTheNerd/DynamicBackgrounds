from dataclasses import dataclass, field
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
    gradient: Optional[dict[str, Any]] = None
    shader: Optional[dict[str, Any]] = None
    _gradient: Optional[ColorABC] = field(init=False, default=None)
    _shader: Optional[ShaderABC] = field(init=False, default=None)

    def __post_init__(self) -> None:
        if self.gradient is not None:
            self._gradient = get_triangle_color_object(self.gradient)
        if self.shader is not None:
            self._shader = get_shader_object(self.shader)

    def get_color(self, triangle: Triangle, t: float) -> Color:
        color = (255, 255, 255)
        if self._gradient is not None:
            color = self._gradient.get_color(triangle, t)
        facing_ratio = 1.0
        if self._shader is not None:
            facing_ratio = self._shader.get_facing_ratio(triangle, t)
        return ColorRGB.interpolate(
            ColorRGB(0, 0, 0), ColorRGB.generate(color), facing_ratio
        ).make_drawable()


def get_triangle_object(configs: dict[str, Any] | ObjectConfigs) -> TriangleDrawerABC:
    return get_object(TriangleDrawerABC, configs)
