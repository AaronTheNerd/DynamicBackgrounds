from dataclasses import dataclass
from typing import Any

from coloring.ABCs import LineWidthABC
from configs import ObjectConfigs
from triangle import Edge
from utils.concrete_inheritors import get_object


@dataclass
class Static(LineWidthABC):
    width: int = 1

    def get_width(self, edge: Edge, t: float) -> int:
        return self.width


def get_line_width_object(configs: ObjectConfigs | dict[str, Any]) -> LineWidthABC:
    return get_object(LineWidthABC, configs)