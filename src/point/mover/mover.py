import math
from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.mover.ABCs import MoverABC, MoverState
from utils.concrete_inheritors import get_object


@dataclass
class Drift(MoverABC):
    frequency: int

    def get_offset(self, t: float, state: MoverState) -> float:
        return state.max_value * self.frequency * t


@dataclass
class ReflectiveDrift(MoverABC):
    amplitude: float
    frequency: int

    def get_offset(self, t: float, state: MoverState) -> float:
        return (
            state.max_value
            * self.amplitude
            * math.sin(2 * math.pi * self.frequency * t)
        )


@dataclass
class Sway(MoverABC):
    amplitude: float
    x_scale: float
    y_scale: float
    intensity: float
    x_offset: float
    y_offset: float

    def get_offset(self, t: float, state: MoverState) -> float:
        return (
            state.max_value
            * self.amplitude
            * state.open_simplex.noise4(
                x=state.original_pos.x * self.x_scale + self.x_offset,
                y=state.original_pos.y * self.y_scale + self.y_offset,
                z=self.intensity * math.cos(2 * math.pi * t),
                w=self.intensity * math.sin(2 * math.pi * t),
            )
        )


def get_mover_object(configs: ObjectConfigs | dict[str, Any]) -> MoverABC:
    return get_object(MoverABC, configs)
