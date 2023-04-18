import math
from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.mover.ABCs import MoverState, ZMoverABC
from utils.concrete_inheritors import get_object


@dataclass
class _Sway(ZMoverABC):
    amplitude: float
    x_scale: float
    y_scale: float
    intensity: float
    x_offset: float
    y_offset: float

    def get_offset(self, t: float, state: MoverState) -> float:
        return self.amplitude * state.open_simplex.noise4(
            x=state.original_pos.x * self.x_scale + self.x_offset,
            y=state.original_pos.y * self.y_scale + self.y_offset,
            z=self.intensity * math.cos(2 * math.pi * t),
            w=self.intensity * math.sin(2 * math.pi * t),
        )


@dataclass
class _NoiseMap(ZMoverABC):
    amplitude: float
    x_scale: float
    y_scale: float
    x_offset: float
    y_offset: float

    def get_offset(self, t: float, state: MoverState) -> float:
        return self.amplitude * state.open_simplex.noise2(
            x=state.current_pos.x * self.x_scale + self.x_offset,
            y=state.current_pos.y * self.y_scale + self.y_offset,
        )


@dataclass
class _Wave(ZMoverABC):
    amplitude: float
    speed: int
    wavelength: float
    axis: str

    def get_offset(self, t: float, state: MoverState) -> float:
        pos = state.current_pos.x if self.axis == "x" else state.current_pos.y
        return self.amplitude * math.sin(2 * math.pi * self.speed * t + self.wavelength / state.max_value * pos)


def get_zmover_object(configs: ObjectConfigs | dict[str, Any]) -> ZMoverABC:
    return get_object(ZMoverABC, configs)
