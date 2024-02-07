from __future__ import annotations

import math
from dataclasses import dataclass

from coloring.metric.ABCs import (
    EdgeMetricABC,
    MetricABC,
    TriangleMetricABC,
    VertexMetricABC,
)
from coloring.shifting.ABCs import ShiftingPointABC
from coloring.shifting.point import get_shifting_point_object
from configs import ObjectConfigs
from point.ABCs import PointABC
from serial.JSON_types import JSON_object
from triangle.triangle import Edge, Triangle
from utils.concrete_inheritors import get_object


@dataclass
class Length(EdgeMetricABC):
    min_length: int
    max_length: int

    @classmethod
    def from_json(cls, *args, **kwargs) -> Length:
        return cls(*args, **kwargs)

    def measure_edge(self, edge: Edge, time: float) -> float:
        length = edge.length()
        t = (length - self.min_length) / (self.max_length - self.min_length)
        t = max(0.0, min(t, 1.0))
        return t


@dataclass
class DistanceOnLine(VertexMetricABC, EdgeMetricABC, TriangleMetricABC):
    start: ShiftingPointABC
    end: ShiftingPointABC

    @classmethod
    def from_json(cls, start: JSON_object, end: JSON_object) -> DistanceOnLine:
        return cls(
            start=get_shifting_point_object(start),
            end=get_shifting_point_object(end),
        )

    def measure_vertex(self, point: PointABC, time: float) -> float:
        current_start = self.start.get_point(time)
        current_end = self.end.get_point(time)
        dx = current_end.x - current_start.x
        dy = current_end.y - current_start.y
        t = (dx * (point.x - current_start.x) + dy * (point.y - current_start.y)) / (
            math.pow(dx, 2) + math.pow(dy, 2)
        )
        return max(0.0, min(t, 1.0))

    def measure_edge(self, edge: Edge, time: float) -> float:
        return self.measure_vertex(edge.midpoint(), time)

    def measure_triangle(self, triangle: Triangle, time: float) -> float:
        return self.measure_vertex(triangle.center(), time)


@dataclass
class DistanceFromPoint(VertexMetricABC, EdgeMetricABC, TriangleMetricABC):
    min_distance: float
    max_distance: float
    center: ShiftingPointABC

    @classmethod
    def from_json(
        cls, min_distance: float, max_distance: float, center: JSON_object
    ) -> DistanceFromPoint:
        return cls(
            min_distance=min_distance,
            max_distance=max_distance,
            center=get_shifting_point_object(center),
        )

    def measure_vertex(self, point: PointABC, time: float) -> float:
        current_center = self.center.get_point(t)
        dist = math.sqrt(
            math.pow(point.x - current_center.x, 2)
            + math.pow(point.y - current_center.y, 2)
        )
        t = (dist - self.min_distance) / (self.max_distance - self.min_distance)
        return max(0.0, min(t, 1.0))

    def measure_edge(self, edge: Edge, time: float) -> float:
        return self.measure_vertex(edge.midpoint(), time)

    def measure_triangle(self, triangle: Triangle, time: float) -> float:
        return self.measure_vertex(triangle.center(), time)


@dataclass
class Time(VertexMetricABC, EdgeMetricABC, TriangleMetricABC):
    @classmethod
    def from_json(cls, *args, **kwargs) -> Time:
        return cls(*args, **kwargs)

    def measure_vertex(self, point: PointABC, time: float) -> float:
        return time

    def measure_edge(self, edge: Edge, time: float) -> float:
        return time

    def measure_triangle(self, triangle: Triangle, time: float) -> float:
        return time


def get_metric_object(configs: ObjectConfigs | JSON_object) -> MetricABC:
    return get_object(MetricABC, configs)
