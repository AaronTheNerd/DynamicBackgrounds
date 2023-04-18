from abc import ABC, abstractmethod

from point.ABCs import PointABC
from triangle import Edge


# Takes an edge and converts to a value between 0 and 1
class LineRangeABC(ABC):
    @abstractmethod
    def get_value(self, edge: Edge, t: float) -> float:
        ...


# Takes some position and converts to a value between 0 and 1
class PositionRangeABC(ABC):
    @abstractmethod
    def get_value(self, point: PointABC, t: float) -> float:
        ...


# Takes a value between 0 and 1 and converts to a value between 0 and 1
class RangeABC(ABC):
    @abstractmethod
    def get_value(self, t: float) -> float:
        ...


# Takes a value between 0 and 1 and converts to a value between 0 and 1 but its ends must be equal
class ReflectiveRangeABC(ABC):
    @abstractmethod
    def get_value(self, t: float) -> float:
        ...
