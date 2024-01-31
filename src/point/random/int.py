from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.random.ABCs import RandomIntABC
from utils.concrete_inheritors import get_object


@dataclass
class Integer(RandomIntABC):
    value: int

    @classmethod
    def from_json(cls, *args, **kwargs) -> Integer:
        return cls(*args, **kwargs)

    def get_value(self) -> int:
        return self.value


@dataclass
class Choice(RandomIntABC):
    choices: list[int]

    @classmethod
    def from_json(cls, *args, **kwargs) -> Choice:
        return cls(*args, **kwargs)

    def get_value(self) -> int:
        return random.choice(self.choices)


@dataclass
class RandInt(RandomIntABC):
    min_value: int
    max_value: int

    @classmethod
    def from_json(cls, *args, **kwargs) -> RandInt:
        return cls(*args, **kwargs)

    def get_value(self) -> int:
        return random.randint(self.min_value, self.max_value)


def get_rand_int_object(configs: ObjectConfigs | dict[str, Any]) -> RandomIntABC:
    return get_object(RandomIntABC, configs)
