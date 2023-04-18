from dataclasses import dataclass

from configs import CONFIGS
from point.ABCs import PointABC
from point.mover.ABCs import MoverABC, ZMoverABC
from point.state import MoverState

from opensimplex import OpenSimplex

class Static(PointABC):
    def at(self, t: float) -> PointABC:
        return Static(self.x, self.y, self.z)
    

@dataclass
class Moving(PointABC):
    x_movers: list[MoverABC]
    y_movers: list[MoverABC]
    z_movers: list[ZMoverABC]
    open_simplex: OpenSimplex

    def at(self, t: float) -> PointABC:
        original_point = Static(self.x, self.y, self.z)
        current_point = Static(self.x, self.y, self.z)
        state = MoverState(CONFIGS.full_width, self.open_simplex, original_point, current_point)
        for mover in self.x_movers:
            offset = mover.get_offset(t, state)
            current_point.x += offset
        state.current_pos = current_point
        for mover in self.y_movers:
            offset = mover.get_offset(t, state)
            current_point.y += offset
        if current_point.x < 0.0 or current_point.x > CONFIGS.full_width:
            current_point.x = current_point.x % CONFIGS.full_width
        if current_point.y < 0.0 or current_point.y > CONFIGS.full_height:
            current_point.y = current_point.y % CONFIGS.full_height
        state.current_pos = current_point
        for mover in self.z_movers:
            offset = mover.get_offset(t, state)
            current_point.z += offset
        return current_point
