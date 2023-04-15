from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from opensimplex import OpenSimplex

from configs import CONFIGS

open_simplex = None


def seed(seed: int) -> None:
    global open_simplex
    open_simplex = OpenSimplex(seed=seed)


@dataclass
class PointABC(ABC):
    x: float = 0.0
    y: float = 0.0
    z: float = field(default=None, compare=False, repr=False)  # type: ignore

    def __post_init__(self):
        global open_simplex
        if self.z is None:
            self.z = open_simplex.noise2(x=self.x, y=self.y)  # type: ignore

    @abstractmethod
    def at(self, t: float) -> PointABC:
        ...


class StaticPoint(PointABC):
    def at(self, t: float) -> PointABC:
        return StaticPoint(self.x, self.y, self.z)


class SwayingPoint(StaticPoint):
    def at(self, t: float) -> PointABC:
        global open_simplex
        new_x = self.x + CONFIGS.point_configs.amplitude * open_simplex.noise4(  # type: ignore
            x=self.x * CONFIGS.point_configs.scale,
            y=self.y * CONFIGS.point_configs.scale,
            z=CONFIGS.point_configs.intensity * math.cos(2 * math.pi * t),
            w=CONFIGS.point_configs.intensity * math.sin(2 * math.pi * t),
        )
        new_y = self.y + CONFIGS.point_configs.amplitude * open_simplex.noise4(  # type: ignore
            x=self.x * CONFIGS.point_configs.scale + CONFIGS.point_configs.offset_y,
            y=self.y * CONFIGS.point_configs.scale,
            z=CONFIGS.point_configs.intensity * math.cos(2 * math.pi * t),
            w=CONFIGS.point_configs.intensity * math.sin(2 * math.pi * t),
        )
        if new_x < 0.0 or new_x > CONFIGS.full_width:
            new_x = float((int(new_x) + CONFIGS.full_width) % CONFIGS.full_width)
        if new_y < 0.0 or new_y > CONFIGS.full_height:
            new_y = float((int(new_y) + CONFIGS.full_height) % CONFIGS.full_height)
        return SwayingPoint(new_x, new_y, self.z)


@dataclass
class DriftingPoint(SwayingPoint):
    dx: int | float = field(default=1, repr=False)
    dy: int | float = field(default=1, repr=False)
    relective: bool = field(default=False, repr=False)

    def at(self, t: float) -> PointABC:
        shifted_point = super().at(t)
        offset_x = 0.0
        offset_y = 0.0
        if self.relective:
            offset_x = CONFIGS.full_width * self.dx * math.sin(2 * math.pi * t)
            offset_y = CONFIGS.full_height * self.dy * math.sin(2 * math.pi * t)
        else:
            offset_x = CONFIGS.full_width * t * self.dx
            offset_y = CONFIGS.full_height * t * self.dy
        new_x = shifted_point.x + offset_x
        new_y = shifted_point.y + offset_y
        if new_x < 0.0 or new_x > CONFIGS.full_width:
            new_x = float((int(new_x) + CONFIGS.full_width) % CONFIGS.full_width)
        if new_y < 0.0 or new_y > CONFIGS.full_height:
            new_y = float((int(new_y) + CONFIGS.full_height) % CONFIGS.full_height)
        return DriftingPoint(new_x, new_y, self.z)
