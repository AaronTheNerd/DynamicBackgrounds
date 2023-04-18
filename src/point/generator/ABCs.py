from dataclasses import dataclass
from abc import abstractmethod, ABC
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