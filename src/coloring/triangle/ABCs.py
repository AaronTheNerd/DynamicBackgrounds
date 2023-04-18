from abc import ABC, abstractmethod

from coloring.color import Color
from triangle import Triangle


class ColorABC(ABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, t: float) -> Color:
        ...


class ShaderABC(ABC):
    @abstractmethod
    def get_facing_ratio(self, triangle: Triangle, t: float) -> float:
        ...


class TriangleDrawerABC(ABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, t: float) -> Color:
        ...
