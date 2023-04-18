from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.generator.ABCs import ZMoverGeneratorABC
from point.mover.ABCs import ZMoverABC
from point.mover.zmover import _NoiseMap, _Sway
from utils.concrete_inheritors import get_object


@dataclass
class Sway(ZMoverGeneratorABC):
    amplitude: float
    scale: float
    intensity: float
    offset: float

    def generate(self) -> ZMoverABC:
        return _Sway(self.amplitude, self.scale, self.intensity, self.offset)


@dataclass
class NoiseMap(ZMoverGeneratorABC):
    amplitude: float
    x_scale: float
    y_scale: float
    x_offset: float
    y_offset: float

    def generate(self) -> ZMoverABC:
        return _NoiseMap(self.amplitude, self.x_scale, self.y_scale, self.x_offset, self.y_offset)


def get_zmover_generator_object(configs: ObjectConfigs | dict[str, Any]) -> ZMoverGeneratorABC:
    return get_object(ZMoverGeneratorABC, configs)
