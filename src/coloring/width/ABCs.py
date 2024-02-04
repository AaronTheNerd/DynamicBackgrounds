from abc import abstractmethod

from serial.ABCs import SerialABC


class WidthABC(SerialABC):
    @abstractmethod
    def get_width(self, t: float, time: float) -> int: ...
