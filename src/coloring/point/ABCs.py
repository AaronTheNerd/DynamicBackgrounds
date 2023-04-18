from abc import ABC, abstractmethod

from coloring.color import Color
from point.ABCs import PointABC


class ColorABC(ABC):
    @abstractmethod
    def get_color(self, point: PointABC, t: float) -> Color:
        ...


class WidthABC(ABC):
    @abstractmethod
    def get_width(self, point: PointABC, t: float) -> int:
        ...


class PointDrawerABC(ABC):
    @abstractmethod
    def get_color(self, point: PointABC, t: float) -> Color:
        ...

    @abstractmethod
    def get_width(self, point: PointABC, t: float) -> int:
        ...
