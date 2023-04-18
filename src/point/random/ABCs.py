from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RandomIntABC(ABC):
    @abstractmethod
    def get_value(self) -> int:
        ...


@dataclass
class RandomFloatABC(ABC):
    @abstractmethod
    def get_value(self) -> float:
        ...
