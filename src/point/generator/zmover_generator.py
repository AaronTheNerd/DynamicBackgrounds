from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.generator.ABCs import ZMoverGeneratorABC
from point.mover.ABCs import ZMoverABC
from point.mover.zmover import NoiseMap, Sway, Wave
from utils.concrete_inheritors import get_object


@dataclass
class SwayGenerator(ZMoverGeneratorABC):
    amplitude: float
    x_scale: float
    y_scale: float
    intensity: float
    x_offset: float
    y_offset: float

    @classmethod
    def from_json(cls, *args, **kwargs) -> SwayGenerator:
        return cls(*args, **kwargs)

    def generate(self) -> ZMoverABC:
        return Sway(self.amplitude, self.x_scale, self.y_scale, self.intensity, self.x_offset, self.y_offset)


@dataclass
class NoiseMapGenerator(ZMoverGeneratorABC):
    amplitude: float
    x_scale: float
    y_scale: float
    x_offset: float
    y_offset: float

    @classmethod
    def from_json(cls, *args, **kwargs) -> NoiseMapGenerator:
        return cls(*args, **kwargs)

    def generate(self) -> ZMoverABC:
        return NoiseMap(self.amplitude, self.x_scale, self.y_scale, self.x_offset, self.y_offset)


@dataclass
class WaveGenerator(ZMoverGeneratorABC):
    amplitude: float
    speed: int
    wavelength: float
    axis: str = "x"

    @classmethod
    def from_json(cls, *args) -> WaveGenerator:
        return cls(*args)

    def generate(self) -> ZMoverABC:
        return Wave(self.amplitude, self.speed, self.wavelength, self.axis)


def get_zmover_generator_object(configs: ObjectConfigs | dict[str, Any]) -> ZMoverGeneratorABC:
    return get_object(ZMoverGeneratorABC, configs)
