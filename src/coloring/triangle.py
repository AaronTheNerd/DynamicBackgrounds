from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from coloring.ABCs import ColorerABC, ShaderABC, TriangleColorABC
from coloring.color import Color, ColorHSV, ColorRGB
from coloring.colorer import get_colorer_object
from coloring.shader import get_shader_object
from configs import ObjectConfigs
from triangle import Triangle
from utils.concrete_inheritors import get_object


@dataclass
class TriangleColorer(TriangleColorABC):
    gradient: Optional[Dict[str, Any]]
    shader: Optional[Dict[str, Any]]
    _gradient: Optional[ColorerABC] = field(init=False)
    _shader: Optional[ShaderABC] = field(init=False)

    def __post_init__(self) -> None:
        if self.gradient is not None:
            self._gradient = get_colorer_object(self.gradient)
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


def get_triangle_object(configs: Dict[str, Any] | ObjectConfigs) -> Optional[TriangleColorABC]:
    return get_object(TriangleColorABC, configs)
