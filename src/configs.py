import json
import os
import random
from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any, TypeVar, Optional


@dataclass
class BorderConfigs:
    top: bool
    bottom: bool
    left: bool
    right: bool
    separation: int


@dataclass
class DriftingConfigs:
    reflective: bool
    percentage: float
    x_min: float
    x_max: float
    y_min: float
    y_max: float


@dataclass
class PointGenerationConfigs:
    num_of_points: float
    separation_radius: float
    max_fails: int
    border_configs: BorderConfigs


@dataclass
class PointMovementConfigs:
    x_movers: list[dict[str, Any]]
    y_movers: list[dict[str, Any]]
    z_movers: list[dict[str, Any]]


@dataclass
class GIFConfigs:
    width: int
    height: int
    num: int
    background_color: list[int]
    margin: int
    ms_per_frame: int
    num_of_frames: int


@dataclass
class ObjectConfigs:
    type: str
    kwargs: dict[str, Any] = field(default_factory=dict)


@dataclass
class Configs:
    generate_seed: bool
    seed: int
    gif_configs: GIFConfigs
    point_generation_configs: PointGenerationConfigs
    point_movement_configs: PointMovementConfigs
    triangle_coloring: Optional[ObjectConfigs] = None
    line_coloring: Optional[ObjectConfigs] = None
    point_coloring: Optional[ObjectConfigs] = None
    full_width: int = field(init=False)
    full_height: int = field(init=False)

    def __post_init__(self) -> None:
        if self.generate_seed:
            self.seed = random.randint(-2147483648, 2147483647)
            self.generate_seed = False
        self.full_width = self.gif_configs.width + 2 * self.gif_configs.margin
        self.full_height = self.gif_configs.height + 2 * self.gif_configs.margin

    def dumpJSON(self) -> dict[str, Any]:
        return _dumpJSON(self)


def _dumpJSON(obj: object) -> dict[str, Any]:
    result = dict()
    if not is_dataclass(obj):
        return result
    for field in fields(obj):
        if not field.init:
            continue
        value = obj.__dict__[field.name]
        if is_dataclass(value):
            value = _dumpJSON(value)
        result[field.name] = value
    return result


T = TypeVar("T")


def _replaceWithDataclass(raw_configs: dict[str, Any], cls: type[T]) -> T:
    for field in fields(cls):
        if is_dataclass(field.type):
            raw_configs[field.name] = _replaceWithDataclass(raw_configs[field.name], field.type)
    return cls(**raw_configs)


def _getConfigs() -> Configs:
    abs_path = os.path.abspath(os.path.dirname(__file__))
    raw_json = {}
    with open(f"{abs_path}/../config.json") as configs:
        raw_json = json.load(configs)
    return _replaceWithDataclass(raw_json, Configs)


CONFIGS = _getConfigs()
