from abc import abstractmethod
from typing import Generic, TypeVar

from point.point import Static
from utils.serialABC import SerialABC


class PointTranslatorABC(SerialABC):
    @abstractmethod
    def get_point(self, t: float) -> Static:
        ...


T = TypeVar("T")


# Takes a value between 0 and 1 and converts to a color
class GradientABC(SerialABC, Generic[T]):
    @abstractmethod
    def get_color(self, t: float) -> T:
        ...
