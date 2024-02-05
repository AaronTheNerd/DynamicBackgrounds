from abc import abstractmethod
from dataclasses import dataclass

from point.mover.ABCs import MoverABC, ZMoverABC
from serial.ABCs import SerialABC


@dataclass
class MoverGeneratorABC(SerialABC):
    @abstractmethod
    def generate(self) -> MoverABC: ...


@dataclass
class ZMoverGeneratorABC(SerialABC):
    @abstractmethod
    def generate(self) -> ZMoverABC: ...
