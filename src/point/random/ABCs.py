from dataclasses import dataclass
from abc import ABC, abstractmethod

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