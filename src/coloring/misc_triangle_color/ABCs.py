from abc import abstractmethod

from color import Color
from serial.ABCs import SerialABC
from triangle.triangle import Triangle


class MiscTriangleColorABC(SerialABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, time: float) -> Color:
        ...
