import json
import os
import random
from dataclasses import dataclass, field, fields, is_dataclass
from typing import Optional, TypeVar

from serial.JSON_types import JSON_object


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
    border: BorderConfigs


@dataclass
class PointMovementConfigs:
    x: list[JSON_object]
    y: list[JSON_object]
    z: list[JSON_object]


@dataclass
class ImageConfigs:
    file_extension: str


@dataclass
class VideoConfigs:
    framerate: float
    num_of_frames: int
    frame_file_extension: str


@dataclass(kw_only=True)
class OutputConfigs:
    image: ImageConfigs = None
    video: VideoConfigs = None
    width: int
    height: int
    num: int
    background_color: list[int]
    margin: int

    def __post_init__(self) -> None:
        if self.image is None and self.video is None:
            raise Exception("No output defined")
    


@dataclass
class ObjectConfigs:
    type: str
    kwargs: JSON_object = field(default_factory=dict)


@dataclass(kw_only=True)
class Configs:
    generate_seed: bool
    seed: int
    triangulation: str = "SciPy"
    output: OutputConfigs
    point_generation: PointGenerationConfigs
    point_movement: PointMovementConfigs
    triangle_coloring: Optional[JSON_object] = None
    line_coloring: Optional[JSON_object] = None
    point_coloring: Optional[JSON_object] = None
    full_width: int = field(init=False)
    full_height: int = field(init=False)

    def __post_init__(self) -> None:
        if self.generate_seed:
            self.seed = random.randint(-2147483648, 2147483647)
            self.generate_seed = False
        self.full_width = self.output.width + 2 * self.output.margin
        self.full_height = self.output.height + 2 * self.output.margin

    def dumpJSON(self) -> JSON_object:
        return _dumpJSON(self)


def _dumpJSON(obj: object) -> JSON_object:
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


def _replaceWithDataclass(raw_configs: JSON_object, cls: type[T]) -> T:
    for field in fields(cls):
        if is_dataclass(field.type) and field.name in raw_configs:
            raw_configs[field.name] = _replaceWithDataclass(
                raw_configs[field.name], field.type
            )
    return cls(**raw_configs)


def _getConfigs() -> Configs:
    abs_path = os.path.abspath(os.path.dirname(__file__))
    raw_json = {}
    with open(f"{abs_path}/../config.json") as configs:
        raw_json = json.load(configs)
    return _replaceWithDataclass(raw_json, Configs)


CONFIGS = _getConfigs()
