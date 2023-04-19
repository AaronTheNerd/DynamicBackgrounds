from dataclasses import dataclass
from typing import Any

from coloring.line.ABCs import WidthABC
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class Static(WidthABC):
    width: int = 1

    def get_width(self, edge: Edge, t: float) -> int:
        return self.width


def get_line_width_object(configs: ObjectConfigs | dict[str, Any]) -> WidthABC:
    return get_object(WidthABC, configs)