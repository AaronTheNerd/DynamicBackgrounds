from dataclasses import dataclass
from abc import ABC, abstractmethod
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
