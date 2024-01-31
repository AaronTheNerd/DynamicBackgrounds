from abc import abstractmethod

from coloring.color import Color
from triangle import Triangle
from utils.serialABC import SerialABC


class ColorABC(SerialABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, t: float) -> Color:
        ...


class ShaderABC(SerialABC):
    @abstractmethod
    def get_facing_ratio(self, triangle: Triangle, t: float) -> float:
        ...
