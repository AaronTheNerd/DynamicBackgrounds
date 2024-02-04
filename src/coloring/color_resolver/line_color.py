from __future__ import annotations

from dataclasses import dataclass

from coloring.gradient.ABCs import GradientABC
from coloring.metric.ABCs import VertexMetricABC
from coloring.metric_modifier.ABCs import ModifierABC
from color import Color
from triangle import Edge
from serial.ABCs import SerialABC
from serial.JSON_types import JSON_object


@dataclass
class LineColorResolver(SerialABC):
    gradient: GradientABC
    metric: VertexMetricABC
    metric_modifiers: list[ModifierABC]

    @classmethod
    def from_json(
        cls,
        gradient: JSON_object,
        metric: JSON_object,
        metric_modifiers: list[JSON_object],
    ) -> LineColorResolver:
        return cls()

    def get_color(self, edge: Edge, time: float) -> Color: ...
