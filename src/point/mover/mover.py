import math
from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.mover.ABCs import MoverABC, MoverState
from utils.concrete_inheritors import get_object


@dataclass
class _Drift(MoverABC):
    frequency: int

    def get_offset(self, t: float, state: MoverState) -> float:
        return state.max_value * self.frequency * t
    

@dataclass
class _ReflectiveDrift(MoverABC):
    frequency: float

    def get_offset(self, t: float, state: MoverState) -> float:
        return state.max_value * self.frequency * math.sin(2 * math.pi * t)


@dataclass
class _Sway(MoverABC):
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


def get_mover_object(configs: ObjectConfigs | dict[str, Any]) -> MoverABC:
    return get_object(MoverABC, configs)