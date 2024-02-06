from abc import abstractmethod

from color import Color
from serial.ABCs import SerialABC
from triangle import Triangle


class TriangleColorResolverABC(SerialABC):
    @abstractmethod
    def get_color(self, triangle: Triangle, time: float) -> Color:
        ...
