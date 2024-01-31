from abc import abstractmethod

from coloring.color import Color
from triangle import Edge
from utils.serialABC import SerialABC

class ColorABC(SerialABC):
    @abstractmethod
    def get_color(self, edge: Edge, t: float) -> Color:
        ...


class WidthABC(SerialABC):
    @abstractmethod
    def get_width(self, edge: Edge, t: float) -> int:
        ...
