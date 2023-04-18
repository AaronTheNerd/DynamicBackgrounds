from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from coloring.color import Color
from point.ABCs import PointABC
from point.point import Static
from triangle import Edge, Triangle


class PointTranslatorABC(ABC):
    @abstractmethod
    def get_point(self, t: float) -> Static:
        ...


# Takes an edge and converts to a value between 0 and 1
class LineRangeABC(ABC):
    @abstractmethod
    def get_value(self, edge: Edge, t: float) -> float:
        ...


# Takes some position and converts to a value between 0 and 1
class PositionRangeABC(ABC):
    @abstractmethod
    def get_value(self, point: PointABC, t: float) -> float:
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


class TriangleColorABC(ABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, t: float) -> Color:
        ...


class ShaderABC(ABC):
    @abstractmethod
    def get_facing_ratio(self, triangle: Triangle, t: float) -> float:
        ...


class TriangleColorerABC(ABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, t: float) -> Color:
        ...


class LineColorABC(ABC):
    @abstractmethod
    def get_color(self, edge: Edge, t: float) -> Color:
        ...


class LineWidthABC(ABC):
    @abstractmethod
    def get_width(self, edge: Edge, t: float) -> int:
        ...


class LineColorerABC(ABC):
    @abstractmethod
    def get_color(self, edge: Edge, t: float) -> Color:
        ...

    @abstractmethod
    def get_width(self, edge: Edge, t: float) -> int:
        ...


class PointColorABC(ABC):
    @abstractmethod
    def get_color(self, point: PointABC, t: float) -> Color:
        ...


class PointWidthABC(ABC):
    @abstractmethod
    def get_width(self, point: PointABC, t: float) -> int:
        ...


class PointColorerABC(ABC):
    @abstractmethod
    def get_color(self, point: PointABC, t: float) -> Color:
        ...

    @abstractmethod
    def get_width(self, point: PointABC, t: float) -> int:
        ...
