from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, TypeVar

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
    color: Color

    @classmethod
    def from_json(cls, color: Color = (255, 255, 255)) -> Plain:
        return cls(color)

    def get_color(self, triangle: Triangle, t: float) -> Color:
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

    def get_color(self, triangle: Triangle, t: float) -> Color:
        current_start_color = self.start_color.get_color(t)
        current_end_color = self.start_color.get_color(t)
        return ColorRGB.interpolate(
            current_start_color, current_end_color, self.range.get_value(triangle.center(), t)
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

    def get_color(self, triangle: Triangle, t: float) -> Color:
        current_start_color = self.start_color.get_color(t)
        current_end_color = self.end_color.get_color(t)
        return ColorHSV.interpolate(
            current_start_color, current_end_color, self.range.get_value(triangle.center(), t)
        ).make_drawable()


@dataclass
class StaticNoise(ColorABC):
    gradient: ColorABC
    scale: float
    open_simplex: OpenSimplex

    @classmethod
    def from_json(cls, gradient: dict[str, Any], scale: float) -> StaticNoise:
        return cls(
            gradient=get_triangle_color_object(gradient),
            scale=scale,
            open_simplex=OpenSimplex(CONFIGS.seed)
        )

    def get_color(self, triangle: Triangle, t: float) -> Color:
        center = triangle.center()
        x, y, z = center.x, center.y, center.z
        t = (
            self.open_simplex.noise3(x=x * self.scale, y=y * self.scale, z=z * self.scale) + 1
        ) / 2
        return self.gradient.get_color(triangle, t)


@dataclass
class TieDyeSwirl(ColorABC):
    start_x: int
    start_y: int
    scale: float
    alpha: float
    colors: list[ColorHSV] = field(init=False)

    @classmethod
    def from_json(
        cls,
        start_x: int = 0,
        start_y: int = 0,
        scale: float = 1,
        alpha: float = 1
    ) -> TieDyeSwirl:
        return cls(
            start_x,
            start_y,
            scale,
            alpha,
            [
                ColorHSV(1.0, 0.0, 0.0),
                ColorHSV(1.0, 1.0, 0),
                ColorHSV(0.1, 1.0, 0.0),
                ColorHSV(0.1, 0.0, 1.0),
                ColorHSV(0.36, 0.0, 0.64),
            ]
        )

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
    gradient: ColorABC

    @classmethod
    def from_json(cls, gradient: dict[str, Any]) -> ColorShifting:
        return cls(get_triangle_color_object(gradient))

    def get_color(self, triangle: Triangle, t: float) -> Color:
        return self.gradient.get_color(triangle, t)


@dataclass
class ImageBlur(ColorABC):
    image: numpy.ndarray

    @classmethod
    def from_json(cls, filepath: str) -> ImageBlur:
        return cls(image=skimage.transform.resize(
            skimage.io.imread(filepath),
            (CONFIGS.full_height, CONFIGS.full_width)
        ))

    def get_color(self, triangle: Triangle, t: float) -> Color:
        polygon = numpy.array([[triangle.a.x, triangle.a.y], [triangle.b.x, triangle.b.y], [triangle.c.x, triangle.c.y]])
        pixels = self.image[skimage.draw.polygon(polygon[:, 1], polygon[:, 0])]
        if len(pixels) == 0:
            return (0,0,0)
        channels = numpy.average(pixels, 0).astype(float)
        return tuple([int(255 * value) for value in channels])


def get_triangle_color_object(configs: ObjectConfigs | dict[str, Any]) -> ColorABC:
    return get_object(ColorABC, configs)
