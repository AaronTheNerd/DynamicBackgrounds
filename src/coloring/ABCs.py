from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from coloring.color import Color
from point import PointABC
from triangle import Edge, Triangle


# Takes some image state and converts to a value between 0 and 1
class ImageRangeABC(ABC):
    @abstractmethod
    def get_value(self, triangle: Triangle, t: float) -> float:
        ...


# Takes a value between 0 and 1 and converts to a value between 0 and 1
class RangeABC(ABC):
    @abstractmethod
    def get_value(self, t: float) -> float:
        ...


# Takes a value between 0 and 1 and converts to a value between 0 and 1 but its ends must be equal
class ReflectiveRangeABC(ABC):
    @abstractmethod
    def get_value(self, t: float) -> float:
        ...


T = TypeVar("T")


# Takes a value between 0 and 1 and converts to a color
class GradientABC(ABC, Generic[T]):
    @abstractmethod
    def get_color(self, t: float) -> T:
        ...


class ColorerABC(ABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, t: float) -> Color:
        ...


class ShaderABC(ABC):
    @abstractmethod
    def get_facing_ratio(self, triangle: Triangle, t: float) -> float:
        ...


class TriangleColorABC(ABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, t: float) -> Color:
        ...


class LineColorABC(ABC):
    @abstractmethod
    def get_color(self, edge: Edge) -> Color:
        ...

    @abstractmethod
    def get_width(self, edge: Edge) -> int:
        ...


class PointColorABC(ABC):
    @abstractmethod
    def get_color(self, point: PointABC) -> Color:
        ...

    @abstractmethod
    def get_width(self, point: PointABC) -> int:
        ...
