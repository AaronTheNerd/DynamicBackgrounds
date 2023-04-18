from dataclasses import dataclass

from opensimplex import OpenSimplex

from point.ABCs import PointABC


@dataclass
class MoverState:
    max_value: int
    open_simplex: OpenSimplex
    original_pos: PointABC
    current_pos: PointABC
