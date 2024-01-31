from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from configs import ObjectConfigs
from point.generator.ABCs import MoverGeneratorABC
from point.mover.ABCs import MoverABC
from point.mover.mover import Drift, ReflectiveDrift, Sway
from point.random.ABCs import RandomFloatABC, RandomIntABC
from point.random.float import get_rand_float_object
from point.random.int import get_rand_int_object
from utils.concrete_inheritors import get_object


@dataclass
class DriftGenerator(MoverGeneratorABC):
    frequency: RandomIntABC

    @classmethod
    def from_json(cls, frequency: dict[str, Any]) -> DriftGenerator:
        return cls(get_rand_int_object(frequency))

    def generate(self) -> MoverABC:
        return Drift(self.frequency.get_value())


@dataclass
class ReflectiveDriftGenerator(MoverGeneratorABC):
    amplitude: RandomFloatABC
    frequency: RandomIntABC

    @classmethod
    def from_json(
        cls,
        amplitude: dict[str, Any],
        frequency: dict[str, Any]
    ) -> ReflectiveDriftGenerator:
        return cls(
            get_rand_float_object(amplitude),
            get_rand_int_object(frequency)
        )

    def generate(self) -> MoverABC:
        return ReflectiveDrift(
            self.amplitude.get_value(), self.frequency.get_value()
        )


@dataclass
class SwayGenerator(MoverGeneratorABC):
    amplitude: float
    x_scale: float
    y_scale: float
    intensity: float
    x_offset: float
    y_offset: float

    @classmethod
    def from_json(cls, *args, **kwargs) -> SwayGenerator:
        return cls(*args, **kwargs)

    def generate(self) -> MoverABC:
        return Sway(
            self.amplitude, self.x_scale, self.y_scale, self.intensity, self.x_offset, self.y_offset
        )


def get_mover_generator_object(configs: ObjectConfigs | dict[str, Any]) -> MoverGeneratorABC:
    return get_object(MoverGeneratorABC, configs)
