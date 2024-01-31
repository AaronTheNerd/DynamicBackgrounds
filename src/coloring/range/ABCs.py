from abc import abstractmethod

from point.ABCs import PointABC
from triangle import Edge
from utils.serialABC import SerialABC


# Takes an edge and converts to a value between 0 and 1
class LineRangeABC(SerialABC):
    @abstractmethod
    def get_value(self, edge: Edge, t: float) -> float:
        ...


# Takes some position and converts to a value between 0 and 1
class PositionRangeABC(SerialABC):
    @abstractmethod
    def get_value(self, point: PointABC, t: float) -> float:
        ...


# Takes a value between 0 and 1 and converts to a value between 0 and 1
class RangeABC(SerialABC):
    @abstractmethod
    def get_value(self, t: float) -> float:
        ...


# Takes a value between 0 and 1 and converts to a value between 0 and 1 but its ends must be equal
class ReflectiveRangeABC(SerialABC):
    @abstractmethod
    def get_value(self, t: float) -> float:
        ...
