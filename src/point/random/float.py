from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.random.ABCs import RandomFloatABC
from utils.concrete_inheritors import get_object


@dataclass
class Float(RandomFloatABC):
    value: float

    @classmethod
    def from_json(cls, *args, **kwargs) -> Float:
        return cls(*args, **kwargs)

    def get_value(self) -> float:
        return self.value


@dataclass
class Choice(RandomFloatABC):
    choices: list[float]

    @classmethod
    def from_json(cls, *args, **kwargs) -> Choice:
        return cls(*args, **kwargs)

    def get_value(self) -> float:
        return random.choice(self.choices)


@dataclass
class Uniform(RandomFloatABC):
    min_value: float
    max_value: float

    @classmethod
    def from_json(cls, *args, **kwargs) -> Uniform:
        return cls(*args, **kwargs)

    def get_value(self) -> float:
        return random.uniform(self.min_value, self.max_value)


@dataclass
class Normal(RandomFloatABC):
    mean: float
    std_dev: float

    @classmethod
    def from_json(cls, *args, **kwargs) -> Normal:
        return cls(*args, **kwargs)

    def get_value(self) -> float:
        return random.normalvariate(self.mean, self.std_dev)


def get_rand_float_object(configs: ObjectConfigs | dict[str, Any]) -> RandomFloatABC:
    return get_object(RandomFloatABC, configs)
