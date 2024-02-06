from typing import Callable

from point.ABCs import PointABC
from triangle import Triangle
from triangulation.bowyer_watson import BowyerWatson
from triangulation.scipy import SciPy


def get_triangulation(triangulation_name: str) -> Callable[[list[PointABC]], list[Triangle]]:
    if triangulation_name == "BowyerWatson":
        return BowyerWatson
    return SciPy
    