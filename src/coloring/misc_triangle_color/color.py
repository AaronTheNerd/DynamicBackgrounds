from __future__ import annotations

from dataclasses import dataclass

import numpy
import skimage
from color import Color

from coloring.misc_triangle_color.ABCs import MiscTriangleColorABC
from configs import CONFIGS, ObjectConfigs
from serial.JSON_types import JSON_object
from triangle import Triangle
from utils.concrete_inheritors import get_object


@dataclass
class ImageBlur(MiscTriangleColorABC):
    image: numpy.ndarray

    @classmethod
    def from_json(cls, filepath: str) -> ImageBlur:
        return cls(
            image=skimage.transform.resize(skimage.io.imread(filepath), (CONFIGS.full_height + 2, CONFIGS.full_width + 2))
        )
    
    def get_color(self, triangle: Triangle, time: float) -> Color:
        polygon = numpy.array([[triangle.a.x, triangle.a.y], [triangle.b.x, triangle.b.y], [triangle.c.x, triangle.c.y]])
        pixels = self.image[skimage.draw.polygon(polygon[:, 1], polygon[:, 0])]
        if len(pixels) == 0:
            return Color(0, 0, 0)
        channels = numpy.average(pixels, 0).astype(float)
        return Color(*[channel for channel in channels])
    
def get_misc_triangle_color_object(configs: ObjectConfigs | JSON_object) -> MiscTriangleColorABC:
    return get_object(MiscTriangleColorABC, configs)
