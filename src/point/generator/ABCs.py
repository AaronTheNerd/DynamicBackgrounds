from abc import ABC, abstractmethod
from dataclasses import dataclass

from point.mover.ABCs import MoverABC, ZMoverABC


@dataclass
class MoverGeneratorABC(ABC):
    @abstractmethod
    def generate(self) -> MoverABC:
        ...


@dataclass
class ZMoverGeneratorABC(ABC):
    @abstractmethod
    def generate(self) -> ZMoverABC:
        ...
