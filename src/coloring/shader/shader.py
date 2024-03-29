from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import utils.vector3d as utils
from coloring.shader.ABCs import ShaderABC
from configs import ObjectConfigs
from triangle.triangle import Triangle
from utils.concrete_inheritors import get_object


@dataclass
class AmbientShader(ShaderABC):
    ambient_vector: utils.Vector3d
    ambient_gain: float
    ambient_definition: int

    @classmethod
    def from_json(
        cls,
        ambient_vector: utils.Vector3d = (0, 0, 1),
        ambient_gain: float = 1.0,
        ambient_definition: int = 1,
    ) -> AmbientShader:
        return cls(utils.normalize3d(ambient_vector), ambient_gain, ambient_definition)

    def get_facing_ratio(self, triangle: Triangle, t: float) -> float:
        normal = utils.get_normal(triangle)
        # Normalize inverse ray direction
        # Generate facing ratio
        facing_ratio = (
            self.ambient_gain
            * max(0.0, utils.dot_product3d(normal, self.ambient_vector))
            ** self.ambient_definition
        )
        # Clamp facing ratio between 0 and 1
        return min(facing_ratio, 1.0)


def get_shader_object(configs: dict[str, Any] | ObjectConfigs) -> ShaderABC:
    return get_object(ShaderABC, configs)
