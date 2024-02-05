from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PointABC(ABC):
    x: float
    y: float
    z: float

    @abstractmethod
    def at(self, t: float) -> PointABC: ...

    def __eq__(self, value: PointABC) -> bool:
        return value is self or (value.x == self.x and value.y == self.y)
