import math
from dataclasses import dataclass, field
from typing import Any, Optional, TypeVar

from opensimplex import OpenSimplex
import skimage
import numpy

from coloring.ABCs import GradientABC
from coloring.color import Color, ColorHSV, ColorRGB
from coloring.gradient import get_gradient_object
from coloring.range.ABCs import PositionRangeABC
from coloring.range.position_range import get_image_range_object
from coloring.triangle.ABCs import ColorABC
from configs import CONFIGS, ObjectConfigs
from triangle import Triangle
from utils.concrete_inheritors import get_object

T = TypeVar("T")


@dataclass
class Plain(ColorABC):
    color: Color = (255, 255, 255)

    def get_color(self, triangle: Triangle, t: float) -> Color:
        return self.color


@dataclass
class GradientRGB(ColorABC):
    start_color: dict[str, Any]
    end_color: dict[str, Any]
    range: dict[str, Any]
    _start_color: GradientABC[ColorRGB] = field(init=False)
    _end_color: GradientABC[ColorRGB] = field(init=False)
    _range: PositionRangeABC = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = get_gradient_object(self.start_color)
        self._end_color = get_gradient_object(self.end_color)
        self._range = get_image_range_object(self.range)

    def get_color(self, triangle: Triangle, t: float) -> Color:
        current_start_color = self._start_color.get_color(t)
        current_end_color = self._start_color.get_color(t)
        return ColorRGB.interpolate(
            current_start_color, current_end_color, self._range.get_value(triangle.center(), t)
        ).make_drawable()


@dataclass
class GradientHSV(ColorABC):
    start_color: dict[str, Any]
    end_color: dict[str, Any]
    range: dict[str, Any]
    _start_color: GradientABC[ColorHSV] = field(init=False)
    _end_color: GradientABC[ColorHSV] = field(init=False)
    _range: PositionRangeABC = field(init=False)

    def __post_init__(self) -> None:
        self._start_color = get_gradient_object(self.start_color)
        self._end_color = get_gradient_object(self.end_color)
        self._range = get_image_range_object(self.range)

    def get_color(self, triangle: Triangle, t: float) -> Color:
        current_start_color = self._start_color.get_color(t)
        current_end_color = self._end_color.get_color(t)
        return ColorHSV.interpolate(
            current_start_color, current_end_color, self._range.get_value(triangle.center(), t)
        ).make_drawable()


@dataclass
class StaticNoise(ColorABC):
    gradient: dict[str, Any]
    scale: float
    _gradient: ColorABC = field(init=False)
    _open_simplex: OpenSimplex = field(init=False)

    def __post_init__(self) -> None:
        self._gradient = get_triangle_color_object(self.gradient)
        self._open_simplex = OpenSimplex(CONFIGS.seed)

    def get_color(self, triangle: Triangle, t: float) -> Color:
        center = triangle.center()
        x, y, z = center.x, center.y, center.z
        t = (
            self._open_simplex.noise3(x=x * self.scale, y=y * self.scale, z=z * self.scale) + 1
        ) / 2
        return self._gradient.get_color(triangle, t)


@dataclass
class TieDyeSwirl(ColorABC):
    start_x: int = 0
    start_y: int = 0
    scale: float = 1
    alpha: float = 1
    colors: list[ColorHSV] = field(init=False)

    def __post_init__(self) -> None:
        self.colors = [
            ColorHSV(1.0, 0.0, 0.0),
            ColorHSV(1.0, 1.0, 0),
            ColorHSV(0.1, 1.0, 0.0),
            ColorHSV(0.1, 0.0, 1.0),
            ColorHSV(0.36, 0.0, 0.64),
        ]

    def get_color(self, triangle: Triangle, t: float) -> Color:
        center = triangle.center()
        x, y = center.x, center.y
        w = [
            x - self.start_x,
            y - self.start_y,
        ]  # Vector pointing from center of tie dye to triangle center
        v = [0, 1]  # Vertical vector
        theta = math.atan2(
            w[1] * v[0] - w[0] * v[1], w[0] * v[0] + w[1] * v[1]
        )  # Angle between v and w
        theta += 2 * math.pi if theta < 0.0 else 0.0
        radial_offset = math.fmod(
            theta, 2 * math.pi / (len(self.colors) + 1)
        )  # 0 <= radial_offset < 2 * math.pi / len(self.colors)
        radial_offset *= (len(self.colors) + 1) / (2 * math.pi)  # 0 <= radial_offset < 1
        radial_offset *= self.scale
        dist = math.sqrt(sum([w[i] ** 2 for i in range(2)]))
        dist_scaled = math.pow(dist, self.alpha)
        offset_dist = dist_scaled + radial_offset
        offset = math.floor(theta / (2 * math.pi) * (len(self.colors) + 1))
        color_index = (int(offset_dist / self.scale) + offset) % len(self.colors)
        return self.colors[color_index].make_drawable()


@dataclass
class ColorShifting(ColorABC):
    gradient: dict[str, Any]
    _gradient: Optional[ColorABC] = field(init=False)

    def __post_init__(self) -> None:
        self._gradient = get_triangle_color_object(self.gradient)

    def get_color(self, triangle: Triangle, t: float) -> Color:
        if self._gradient is None:
            return (0, 0, 0)
        return self._gradient.get_color(triangle, t)


@dataclass
class ImageBlur(ColorABC):
    filepath: str
    _image: numpy.ndarray = field(init=False)

    def __post_init__(self) -> None:
        self._image = skimage.transform.resize(skimage.io.imread(self.filepath), (CONFIGS.full_height, CONFIGS.full_width))

    def get_color(self, triangle: Triangle, t: float) -> Color:
        polygon = numpy.array([[triangle.a.x, triangle.a.y], [triangle.b.x, triangle.b.y], [triangle.c.x, triangle.c.y]])
        pixels = self._image[skimage.draw.polygon(polygon[:, 1], polygon[:, 0])]
        channels = numpy.average(pixels, 0).astype(float)
        return tuple([int(255 * value) for value in channels])


def get_triangle_color_object(configs: ObjectConfigs | dict[str, Any]) -> ColorABC:
    return get_object(ColorABC, configs)
