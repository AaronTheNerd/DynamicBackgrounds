from abc import abstractmethod

from color import Color
from point.point import Static
from serial.ABCs import SerialABC


class ShiftingPointABC(SerialABC):
    @abstractmethod
    def get_point(self, time: float) -> Static: ...


class ShiftingColorABC(SerialABC):
    @abstractmethod
    def get_color(self, time: float) -> Color: ...
