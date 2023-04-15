import math
from typing import Tuple

from triangle import Triangle

Vector3d = Tuple[float, float, float]


def cross3d(v1: Vector3d, v2: Vector3d) -> Vector3d:
    return tuple(
        [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        ]
    )


def normalize3d(v: Vector3d) -> Vector3d:
    mag = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    return tuple([n / mag for n in v])


def dot_product3d(v1: Vector3d, v2: Vector3d) -> float:
    return sum([v1[i] * v2[i] for i in range(3)])


def get_normal(triangle: Triangle) -> Vector3d:
    a, b, c = triangle.a, triangle.b, triangle.c
    edge1 = (b.x - a.x, b.y - a.y, b.z - a.z)
    edge2 = (c.x - a.x, c.y - a.y, c.z - a.z)
    # Perform cross product to find normal vector
    normal = cross3d(edge1, edge2)
    # Check normal vector is facing toward "camera" (z is positive)
    if normal[2] < 0:
        normal = tuple([-normal[i] for i in range(3)])
    # Normalize normal
    return normalize3d(normal)
