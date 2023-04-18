from dataclasses import dataclass
from point.ABCs import PointABC

from opensimplex import OpenSimplex

@dataclass
class MoverState:
    max_value: int
    open_simplex: OpenSimplex
    original_pos: PointABC
    current_pos: PointABC