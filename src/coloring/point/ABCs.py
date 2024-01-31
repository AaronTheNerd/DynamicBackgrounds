from abc import abstractmethod

from coloring.color import Color
from point.ABCs import PointABC
from utils.serialABC import SerialABC


class ColorABC(SerialABC):
    @abstractmethod
    def get_color(self, point: PointABC, t: float) -> Color:
        ...


class WidthABC(SerialABC):
    @abstractmethod
    def get_width(self, point: PointABC, t: float) -> int:
        ...


class PointDrawerABC(SerialABC):
    @abstractmethod
    def get_color(self, point: PointABC, t: float) -> Color:
        ...

    @abstractmethod
    def get_width(self, point: PointABC, t: float) -> int:
        ...
