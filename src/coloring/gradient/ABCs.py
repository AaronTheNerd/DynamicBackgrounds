from abc import abstractmethod

from color import Color
from serial.ABCs import SerialABC


class GradientABC(SerialABC):
    @abstractmethod
    def get_color(self, t: float, time: float) -> Color:
        ...
