from dataclasses import dataclass, field
from typing import Any

from configs import ObjectConfigs
from point.generator.ABCs import MoverGeneratorABC
from point.mover.ABCs import MoverABC
from point.mover.mover import _Drift, _ReflectiveDrift, _Sway
from point.random.ABCs import RandomFloatABC, RandomIntABC
from point.random.float import get_rand_float_object
from point.random.int import get_rand_int_object
from utils.concrete_inheritors import get_object


@dataclass
class Drift(MoverGeneratorABC):
    frequency: dict[str, Any]
    frequency_generator: RandomIntABC = field(init=False)

    def __post_init__(self) -> None:
        self.frequency_generator = get_rand_int_object(self.frequency)

    def generate(self) -> MoverABC:
        return _Drift(self.frequency_generator.get_value())


@dataclass
class ReflectiveDrift(MoverGeneratorABC):
    amplitude: dict[str, Any]
    frequency: dict[str, Any]
    amplitude_generator: RandomFloatABC = field(init=False)
    frequency_generator: RandomFloatABC = field(init=False)

    def __post_init__(self) -> None:
        self.amplitude_generator = get_rand_float_object(self.amplitude)
        self.frequency_generator = get_rand_float_object(self.frequency)

    def generate(self) -> MoverABC:
        return _ReflectiveDrift(
            self.amplitude_generator.get_value(), self.frequency_generator.get_value()
        )


@dataclass
class Sway(MoverGeneratorABC):
    amplitude: float
    x_scale: float
    y_scale: float
    intensity: float
    x_offset: float
    y_offset: float

    def generate(self) -> MoverABC:
        return _Sway(
            self.amplitude, self.x_scale, self.y_scale, self.intensity, self.x_offset, self.y_offset
        )


def get_mover_generator_object(configs: ObjectConfigs | dict[str, Any]) -> MoverGeneratorABC:
    return get_object(MoverGeneratorABC, configs)
