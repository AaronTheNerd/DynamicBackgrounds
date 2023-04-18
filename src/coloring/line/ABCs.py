from abc import ABC, abstractmethod

from coloring.color import Color
from triangle import Edge


class ColorABC(ABC):
    @abstractmethod
    def get_color(self, edge: Edge, t: float) -> Color:
        ...


class WidthABC(ABC):
    @abstractmethod
    def get_width(self, edge: Edge, t: float) -> int:
        ...


class LineDrawerABC(ABC):
    @abstractmethod
    def get_color(self, edge: Edge, t: float) -> Color:
        ...

    @abstractmethod
    def get_width(self, edge: Edge, t: float) -> int:
        ...
