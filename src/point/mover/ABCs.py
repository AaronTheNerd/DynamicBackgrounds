from abc import ABC, abstractmethod
from dataclasses import dataclass

from point.state import MoverState


@dataclass
class MoverABC(ABC):
    @abstractmethod
    def get_offset(self, t: float, state: MoverState) -> float:
        ...


@dataclass
class ZMoverABC(ABC):
    @abstractmethod
    def get_offset(self, t: float, state: MoverState) -> float:
        ...
