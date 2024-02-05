from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from coloring.metric.ABCs import VertexMetricABC
from coloring.metric.metric import get_metric_object
from coloring.metric_modifier.ABCs import ModifierABC
from coloring.metric_modifier.modifier import get_metric_modifier_object
from coloring.width.ABCs import WidthABC
from coloring.width.width import get_width_object
from point.ABCs import PointABC
from serial.ABCs import SerialABC
from serial.JSON_types import JSON_object


@dataclass
class VertexWidthResolver(SerialABC):
    width: WidthABC
    metric: Optional[VertexMetricABC]
    metric_modifiers: list[ModifierABC]

    @classmethod
    def from_json(
        cls,
        width: JSON_object,
        metric: Optional[JSON_object] = None,
        metric_modifiers: Optional[list[JSON_object]] = None,
    ) -> VertexWidthResolver:
        parsed_metric = None
        if metric is not None:
            parsed_metric = get_metric_object(metric)
        if metric_modifiers is None:
            metric_modifiers = []
        return cls(
            width=get_width_object(width),
            metric=parsed_metric,
            metric_modifiers=[
                get_metric_modifier_object(modifier) for modifier in metric_modifiers
            ],
        )

    def get_width(self, vertex: PointABC, time: float) -> int:
        t = 0
        if self.metric is not None:
            t = self.metric.measure_vertex(vertex, time)
        for modifier in self.metric_modifiers:
            t = modifier.get_value(t)
        return self.width.get_width(t, time)
