from abc import abstractmethod

from serial.ABCs import SerialABC
from triangle import Triangle


class ShaderABC(SerialABC):
    @abstractmethod
    def get_facing_ratio(self, triangle: Triangle, t: float) -> float: ...
