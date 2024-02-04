from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from coloring.metric_modifier.ABCs import ModifierABC, ReflectiveModifierABC
from configs import ObjectConfigs
from serial.JSON_types import JSON_object
from utils.concrete_inheritors import get_object
from utils.interpolate import interpolate


@dataclass
class Exponential(ModifierABC):
    alpha: float

    @classmethod
    def from_json(cls, alpha: float = 1.0) -> Exponential:
        return cls(alpha)

    def get_value(self, t: float) -> float:
        t = (math.exp(self.alpha * t) - 1) / (math.exp(self.alpha) - 1)
        return t


@dataclass
class Discrete(ModifierABC):
    segments: int

    @classmethod
    def from_json(cls, segments: int) -> Discrete:
        return cls(segments)

    def get_value(self, t: float) -> float:
        t *= self.segments
        t = int(t)
        t /= self.segments - 1
        return t


@dataclass
class EaseInOut(ModifierABC):
    degree: int

    @classmethod
    def from_json(cls, degree: int = 2) -> EaseInOut:
        return cls(degree)

    def get_value(self, t: float) -> float:
        ease_in = lambda x: math.pow(x, self.degree)
        ease_out = lambda x: 1 - math.pow(1 - x, self.degree)
        return interpolate(ease_in(t), ease_out(t), t)


@dataclass
class Reverse(ModifierABC):
    @classmethod
    def from_json(cls, *args, **kwargs) -> Reverse:
        return cls(*args, **kwargs)
    
    def get_value(self, t: float) -> float:
        return 1 - t


@dataclass
class Sine(ReflectiveModifierABC):
    frequency: int

    @classmethod
    def from_json(cls, frequency: int = 1) -> Sine:
        return cls(frequency)

    def get_value(self, t: float) -> float:
        return (math.sin(t * self.frequency * 2 * math.pi) + 1) / 2


@dataclass
class Cosine(ReflectiveModifierABC):
    frequency: int

    @classmethod
    def from_json(cls, frequency: int = 1) -> Cosine:
        return cls(frequency)

    def get_value(self, t: float) -> float:
        return (math.cos(t * self.frequency * 2 * math.pi) + 1) / 2


@dataclass
class Linear(ReflectiveModifierABC):
    @classmethod
    def from_json(cls) -> Linear:
        return cls()

    def get_value(self, t: float) -> float:
        return 2 * t if t <= 0.5 else (1 - t) * 2


def get_metric_modifier_object(configs: JSON_object | ObjectConfigs) -> ModifierABC:
    return get_object(ModifierABC, configs)

def get_reflective_metric_modifier_object(configs: JSON_object | ObjectConfigs) -> ReflectiveModifierABC:
    return get_object(ReflectiveModifierABC, configs)
