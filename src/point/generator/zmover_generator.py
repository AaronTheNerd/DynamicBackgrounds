from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.generator.ABCs import ZMoverGeneratorABC
from point.mover.ABCs import ZMoverABC
from point.mover.zmover import _NoiseMap, _Sway, _Wave
from utils.concrete_inheritors import get_object


@dataclass
class Sway(ZMoverGeneratorABC):
    amplitude: float
    x_scale: float
    y_scale: float
    intensity: float
    x_offset: float
    y_offset: float

    def generate(self) -> ZMoverABC:
        return _Sway(self.amplitude, self.x_scale, self.y_scale, self.intensity, self.x_offset, self.y_offset)


@dataclass
class NoiseMap(ZMoverGeneratorABC):
    amplitude: float
    x_scale: float
    y_scale: float
    x_offset: float
    y_offset: float

    def generate(self) -> ZMoverABC:
        return _NoiseMap(self.amplitude, self.x_scale, self.y_scale, self.x_offset, self.y_offset)


@dataclass
class Wave(ZMoverGeneratorABC):
    amplitude: float
    speed: int
    wavelength: float
    axis: str = "x"

    def generate(self) -> ZMoverABC:
        return _Wave(self.amplitude, self.speed, self.wavelength, self.axis)


def get_zmover_generator_object(configs: ObjectConfigs | dict[str, Any]) -> ZMoverGeneratorABC:
    return get_object(ZMoverGeneratorABC, configs)
