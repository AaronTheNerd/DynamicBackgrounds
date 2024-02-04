from abc import abstractmethod

from point.ABCs import PointABC
from serial.ABCs import SerialABC
from triangle import Edge, Triangle


class MetricABC(SerialABC): ...


class TriangleMetricABC(MetricABC):
    @abstractmethod
    def measure_triangle(self, triangle: Triangle, time: float) -> float: ...


class EdgeMetricABC(MetricABC):
    @abstractmethod
    def measure_edge(self, edge: Edge, time: float) -> float: ...


class VertexMetricABC(MetricABC):
    @abstractmethod
    def measure_vertex(self, point: PointABC, time: float) -> float: ...
