from abc import abstractmethod
from dataclasses import dataclass

from utils.serialABC import SerialABC

@dataclass
class RandomIntABC(SerialABC):
    @abstractmethod
    def get_value(self) -> int:
        ...


@dataclass
class RandomFloatABC(SerialABC):
    @abstractmethod
    def get_value(self) -> float:
        ...
