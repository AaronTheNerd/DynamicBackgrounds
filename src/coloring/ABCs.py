from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from point.point import Static


class PointTranslatorABC(ABC):
    @abstractmethod
    def get_point(self, t: float) -> Static:
        ...


T = TypeVar("T")


# Takes a value between 0 and 1 and converts to a color
class GradientABC(ABC, Generic[T]):
    @abstractmethod
    def get_color(self, t: float) -> T:
        ...
