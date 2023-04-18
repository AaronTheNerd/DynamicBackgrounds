import random
from dataclasses import dataclass
from typing import Any

from configs import ObjectConfigs
from point.random.ABCs import RandomIntABC
from utils.concrete_inheritors import get_object


@dataclass
class Choice(RandomIntABC):
    choices: list[int]

    def get_value(self) -> int:
        return random.choice(self.choices)


def get_rand_int_object(configs: ObjectConfigs | dict[str, Any]) -> RandomIntABC:
    return get_object(RandomIntABC, configs)
