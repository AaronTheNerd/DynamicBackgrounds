import math
from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.mover.ABCs import MoverState, ZMoverABC
from utils.concrete_inheritors import get_object


@dataclass
class _Sway(ZMoverABC):
    amplitude: float
    scale: float
    intensity: float
    offset: float

    def get_offset(self, t: float, state: MoverState) -> float:
        return self.amplitude * state.open_simplex.noise3(
            x=state.original_pos.x * self.scale + self.offset,
            y=self.intensity * math.cos(2 * math.pi * t),
            z=self.intensity * math.sin(2 * math.pi * t),
        )


def get_zmover_object(configs: ObjectConfigs | dict[str, Any]) -> ZMoverABC:
    return get_object(ZMoverABC, configs)