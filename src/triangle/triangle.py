from __future__ import annotations

import math
from dataclasses import dataclass, field

from point.ABCs import PointABC
from point.point import Static
from triangle.math import LineInterX, LineInterY, lineFromPoints, perpenBisectorFromLine


@dataclass(slots=True)
class Edge:
    a: PointABC
    b: PointABC

    def __eq__(self, value: Edge) -> bool:
        return (self.a.x == value.a.x and self.b.x == value.b.x) or (
            self.b.x == value.a.x and self.a.x == value.b.x
        )

    def midpoint(self) -> Static:
        return Static((self.a.x + self.b.x) / 2, (self.a.y + self.b.y) / 2, 0)

    def length(self) -> float:
        return math.sqrt(
            math.pow(self.a.x - self.b.x, 2) + math.pow(self.a.y - self.b.y, 2)
        )


@dataclass(slots=True)
class Triangle:
    a: PointABC
    b: PointABC
    c: PointABC

    circumcenter: PointABC = field(init=False)
    radius_sq: float = field(init=False)

    def __post_init__(self):
        self.circumcenter, self.radius_sq = self.circumscribe()

    def edges(self) -> tuple[Edge, Edge, Edge]:
        return (Edge(self.a, self.b), Edge(self.a, self.c), Edge(self.b, self.c))

    def has_point(self, p: PointABC) -> bool:
        return (
            (self.a == p)
            or (self.b is p)
            or (self.b == p)
            or (self.c is p)
            or (self.c == p)
            or (self.a is p)
        )

    def has_edge(self, e: Edge) -> bool:
        edges = self.edges()
        for edge in edges:
            if edge == e:
                return True
        return False

    def center(self) -> Static:
        return Static(
            (self.a.x + self.b.x + self.c.x) / 3,
            (self.a.y + self.b.y + self.c.y) / 3,
            (self.a.z + self.b.z + self.c.z) / 3,
        )

    def circumscribe(self) -> tuple[Static, float]:
        P = self.a
        Q = self.b
        R = self.c
        # Store the coordinates
        # radius of circumcircle
        r = Static(0, 0, 0)
        # Line PQ is represented
        # as ax + by = c
        a, b, c = lineFromPoints(P, Q)
        # Line QR is represented
        # as ex + fy = g
        e, f, g = lineFromPoints(Q, R)
        # Converting lines PQ and QR
        # to perpendicular bisectors.
        # After this, L = ax + by = c
        # M = ex + fy = g
        a, b, c = perpenBisectorFromLine(P, Q, a, b, c)
        e, f, g = perpenBisectorFromLine(Q, R, e, f, g)
        # The of intersection
        # of L and M gives r as the
        # circumcenter
        r.x = LineInterX(a, b, c, e, f, g)
        r.y = LineInterY(a, b, c, e, f, g)
        # Length of radius
        q = (r.x - P.x) ** 2 + (r.y - P.y) ** 2
        return r, q
