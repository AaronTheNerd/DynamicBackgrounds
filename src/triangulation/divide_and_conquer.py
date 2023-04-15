from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Optional, Tuple
import math

import numpy as np

from point import PointABC, StaticPoint
from triangle import Edge


def CCW(A: PointABC, B: PointABC, C: PointABC) -> bool:
    return np.linalg.det(np.array([[A.x, A.y, 1], [B.x, B.y, 1], [C.x, C.y, 1]])) > 0  # type: ignore


def rightOf(X: PointABC, e: QuadEdgePtr) -> bool:
    if e.is_nullptr():
        return False
    return CCW(X, e.dest, e.org)


def leftOf(X: PointABC, e: QuadEdgePtr) -> bool:
    if e.is_nullptr():
        return False
    return CCW(X, e.org, e.dest)


def inCircle(A: PointABC, B: PointABC, C: PointABC, D: PointABC) -> bool:
    return (
        np.linalg.det(
            np.array(
                [  # type:ignore
                    [A.x, A.y, (A.x**2) + (A.y**2), 1],
                    [B.x, B.y, (B.x**2) + (B.y**2), 1],
                    [C.x, C.y, (C.x**2) + (C.y**2), 1],
                    [D.x, D.y, (D.x**2) + (D.y**2), 1],
                ]
            )
        )
        > 0
    )


def valid(e: QuadEdgePtr, base1: QuadEdgePtr) -> bool:
    return rightOf(e.dest, base1)


@dataclass
class QuadEdgePtr:
    addr: int = -1
    r: int = 0
    curr_addr: ClassVar[int] = 0
    memory: ClassVar[Dict[int, QuadEdge]] = {}

    def is_nullptr(self) -> bool:
        return not (self.addr in QuadEdgePtr.memory.keys())

    def dereference(self) -> QuadEdge:
        if self.is_nullptr():
            raise Exception("Nullptr")
        return QuadEdgePtr.memory[self.addr]

    @classmethod
    def nullptr(cls):
        return cls()

    @classmethod
    def memdumps(cls) -> str:
        ret = f"{{"
        for index1, (addr, quad_edge) in enumerate(cls.memory.items()):
            if index1 != 0:
                ret += ","
            ret += f"\n  {addr}: {{"
            ret += f"\n    edges: ["
            for index2, edge in enumerate(quad_edge.e):
                if index2 != 0:
                    ret += ","
                ret += f"\n      {{"
                ret += f"\n        data: ({round(edge.data.x, 2)}, {round(edge.data.y, 2)}),"
                ret += f"\n        next: {edge.next.addr},"
                ret += f"\n        r: {edge.next.r}"
                ret += f"\n      }}"
            ret += f"\n    ]"
            ret += f"\n  }}"
        ret += f"\n}}"
        return ret

    @classmethod
    def clear_memory(cls) -> None:
        QuadEdgePtr.memory = dict()

    @classmethod
    def make_primative_edge(cls) -> QuadEdgePtr:
        new_id = cls.curr_addr
        cls.memory[new_id] = QuadEdge(
            [
                EdgeData(StaticPoint(float("-inf"), float("-inf"), 0)),
                EdgeData(StaticPoint(float("inf"), float("inf"), 0)),
                EdgeData(StaticPoint(float("inf"), float("inf"), 0)),
                EdgeData(StaticPoint(float("inf"), float("inf"), 0)),
            ]
        )
        cls.curr_addr += 1
        new_edge = cls(new_id, 0)
        return new_edge

    @classmethod
    def make_edge(cls) -> QuadEdgePtr:
        new_id = cls.curr_addr
        cls.memory[new_id] = QuadEdge(
            [
                EdgeData(StaticPoint(float("-inf"), float("-inf"), 0)),
                EdgeData(StaticPoint(float("inf"), float("inf"), 0)),
                EdgeData(StaticPoint(float("inf"), float("inf"), 0)),
                EdgeData(StaticPoint(float("inf"), float("inf"), 0)),
            ]
        )
        cls.curr_addr += 1
        new_edge = cls(new_id, 0)
        new_edge.Onext = new_edge
        new_edge.Oprev = new_edge
        new_edge.Lnext = new_edge.sym()
        new_edge.Rnext = new_edge.sym()
        return new_edge

    def rot(self) -> QuadEdgePtr:
        return QuadEdgePtr(self.addr, (self.r + 1) % 4)

    def sym(self) -> QuadEdgePtr:
        return QuadEdgePtr(self.addr, (self.r + 2) % 4)

    def inv_rot(self) -> QuadEdgePtr:
        return QuadEdgePtr(self.addr, (self.r + 3) % 4)

    @property
    def org(self) -> PointABC:
        if self.is_nullptr():
            return StaticPoint(float("inf"), float("inf"), 0)
        return QuadEdgePtr.memory[self.addr].e[self.r].data

    @org.setter
    def org(self, p: PointABC) -> None:
        if self.is_nullptr():
            return
        QuadEdgePtr.memory[self.addr].e[self.r].data = p

    @property
    def dest(self) -> PointABC:
        return self.sym().org

    @dest.setter
    def dest(self, p: PointABC) -> None:
        if self.is_nullptr():
            return
        QuadEdgePtr.memory[self.addr].e[(self.r + 2) % 4].data = p

    @property
    def Onext(self) -> QuadEdgePtr:
        if self.is_nullptr():
            return QuadEdgePtr.nullptr()
        specific_edge = self.dereference()
        return specific_edge.e[self.r].next

    @Onext.setter
    def Onext(self, value: QuadEdgePtr) -> None:
        if self.is_nullptr() or value.is_nullptr():
            return
        onext = QuadEdgePtr.memory[self.addr].e[self.r].next
        if onext.is_nullptr():
            onext = QuadEdgePtr.make_primative_edge()
            QuadEdgePtr.memory[self.addr].e[self.r].next = onext
        QuadEdgePtr.memory[onext.addr].e[onext.r] = QuadEdgePtr.memory[value.addr].e[value.r]

    @property
    def Oprev(self) -> QuadEdgePtr:
        if self.is_nullptr():
            return QuadEdgePtr.nullptr()
        specific_edge = self.dereference()
        specific_next = specific_edge.e[(self.r + 1) % 4].next
        if specific_next.is_nullptr():
            return QuadEdgePtr.nullptr()
        return specific_next.rot()

    @Oprev.setter
    def Oprev(self, value: QuadEdgePtr) -> None:
        if self.is_nullptr() or value.is_nullptr():
            return
        rot_next = QuadEdgePtr.memory[self.addr].e[(self.r + 1) % 4].next
        if rot_next.is_nullptr():
            rot_next = QuadEdgePtr.make_primative_edge()
            QuadEdgePtr.memory[self.addr].e[self.r].next = rot_next
        QuadEdgePtr.memory[rot_next.addr].e[(rot_next.r + 1) % 4] = QuadEdgePtr.memory[value.addr].e[value.r]

    @property
    def Lnext(self) -> QuadEdgePtr:
        if self.is_nullptr():
            return QuadEdgePtr.nullptr()
        inv_rot = self.inv_rot()
        if inv_rot.is_nullptr():
            return QuadEdgePtr.nullptr()
        inv_rot_next = inv_rot.Onext
        if inv_rot_next.is_nullptr():
            return QuadEdgePtr.nullptr()
        return inv_rot_next.rot()

    @Lnext.setter
    def Lnext(self, value: QuadEdgePtr) -> None:
        if self.is_nullptr() or value.is_nullptr():
            return
        invrot_next = QuadEdgePtr.memory[self.addr].e[(self.r + 3) % 4].next
        if invrot_next.is_nullptr():
            invrot_next = QuadEdgePtr.make_primative_edge()
            QuadEdgePtr.memory[self.addr].e[self.r].next = invrot_next
        QuadEdgePtr.memory[invrot_next.addr].e[(invrot_next.addr + 1) % 4] = QuadEdgePtr.memory[value.addr].e[value.r]

    @property
    def Rnext(self) -> QuadEdgePtr:
        if self.is_nullptr():
            return QuadEdgePtr.nullptr()
        inv_rot = self.rot()
        if inv_rot.is_nullptr():
            return QuadEdgePtr.nullptr()
        inv_rot_next = inv_rot.Onext
        if inv_rot_next.is_nullptr():
            return QuadEdgePtr.nullptr()
        return inv_rot_next.inv_rot()

    @Rnext.setter
    def Rnext(self, value: QuadEdgePtr) -> None:
        if self.is_nullptr() or value.is_nullptr():
            return
        rot_next = QuadEdgePtr.memory[self.addr].e[(self.r + 1) % 4].next
        if rot_next.is_nullptr():
            rot_next = QuadEdgePtr.make_primative_edge()
            QuadEdgePtr.memory[self.addr].e[self.r].next = rot_next
        QuadEdgePtr.memory[rot_next.addr].e[(rot_next.addr + 3) % 4] = QuadEdgePtr.memory[value.addr].e[value.r]

    @property
    def Rprev(self) -> QuadEdgePtr:
        if self.is_nullptr():
            return QuadEdgePtr.nullptr()
        sym = self.sym()
        if sym.is_nullptr():
            return QuadEdgePtr.nullptr()
        return sym.Onext


@dataclass
class EdgeData:
    data: PointABC
    next: QuadEdgePtr = field(default_factory=QuadEdgePtr.nullptr)


@dataclass
class QuadEdge:
    e: List[EdgeData]


@dataclass
class QuadEdgeStructure:
    points: List[PointABC]

    def __post_init__(self):
        self.points.sort(key=lambda a: [a.x, a.y])
        print(self.points)
        QuadEdgePtr.clear_memory()
            
    def splice(self, a: QuadEdgePtr, b: QuadEdgePtr) -> None:
        if a.r % 2 != b.r % 2:
            return
        print(f"Before splicing {a} and {b}: {QuadEdgePtr.memdumps()}")
        a_onext = a.Onext
        b_onext = b.Onext
        alpha = a_onext.rot()
        beta = b_onext.rot()
        alpha_onext = alpha.Onext
        beta_onext = beta.Onext
        a.Onext = b_onext
        b.Onext = a_onext
        alpha.Onext = beta_onext
        beta.Onext = alpha_onext
        print(f"After splice: {QuadEdgePtr.memdumps()}")

    def deleteEdge(self, e: QuadEdgePtr) -> None:
        self.splice(e, e.Oprev)
        self.splice(e.sym(), e.sym().Oprev)
        #del QuadEdgePtr.memory[e.addr]

    def connect(self, a: QuadEdgePtr, b: QuadEdgePtr) -> QuadEdgePtr:
        new_edge = QuadEdgePtr.make_edge()
        new_edge.org = a.dest
        new_edge.dest = b.org
        self.splice(new_edge, a.Lnext)
        self.splice(new_edge.sym(), b)
        return new_edge

    def run(self, points: List[PointABC]) -> Tuple[QuadEdgePtr, QuadEdgePtr]:
        print(points)
        if len(points) == 2:
            a = QuadEdgePtr.make_edge()
            a.org = points[0]
            a.dest = points[1]
            return (a, a.sym())
        elif len(points) == 3:
            a = QuadEdgePtr.make_edge()
            b = QuadEdgePtr.make_edge()
            self.splice(a.sym(), b)
            a.org = points[0]
            a.dest = points[1]
            b.org = points[1]
            b.dest = points[2]
            if CCW(points[0], points[1], points[2]):
                self.connect(b, a)
                return (a, b.sym())
            elif CCW(points[0], points[2], points[1]):
                c = self.connect(b, a)
                return (c.sym(), c)
            else:
                return (a, b.sym())
        else:
            mid = len(points) // 2
            ldo, ldi = self.run(points[:mid])
            rdi, rdo = self.run(points[mid:])
            while True:
                if leftOf(rdi.org, ldi):
                    ldi = ldi.Lnext
                elif rightOf(ldi.org, rdi):
                    rdi = rdi.Rprev
                else:
                    break
            base1 = self.connect(rdi.sym(), ldi)
            if ldi.org == ldo.org:
                ldo = base1.sym()
            if rdi.org == rdo.org:
                rdo = base1
            while True:
                lcand = base1.sym().Onext
                if valid(lcand, base1):
                    while inCircle(base1.dest, base1.org, lcand.dest, lcand.Onext.dest):
                        t = lcand.Onext
                        self.deleteEdge(lcand)
                        lcand = t
                rcand = base1.Oprev
                if valid(rcand, base1):
                    while inCircle(base1.dest, base1.org, rcand.dest, rcand.Oprev.dest):
                        t = rcand.Oprev
                        self.deleteEdge(rcand)
                        rcand = t
                if not valid(lcand, base1) and not valid(rcand, base1):
                    break
                if not valid(lcand, base1) or (
                    valid(rcand, base1) and inCircle(lcand.dest, lcand.org, rcand.org, rcand.dest)
                ):
                    base1 = self.connect(rcand, base1.sym())
                else:
                    base1 = self.connect(base1.sym(), lcand.sym())
            return (ldo, rdo)

def undefined_float(x: float) -> bool:
    return math.isnan(x) or math.isinf(x)

def undefined_point(p: PointABC) -> bool:
    return undefined_float(p.x) or undefined_float(p.y)

def getAllEdges(le: QuadEdgePtr, re: QuadEdgePtr) -> List[Edge]:

    '''
    future_edges = [le, re]
    visited_addrs = set()
    edges = []
    while len(future_edges) > 0:

        # Get next edge
        edge = future_edges.pop()

        # If edge already visited, continue
        if edge.addr in visited_addrs:
            continue

        # Add addr to visited
        visited_addrs.add(edge.addr)

        # Add edge if valid
        if not undefined_point(edge.org) and not undefined_point(edge.dest):
            edges.append((edge.org, edge.dest))

        # Add neighboring edges
        if not edge.Onext.is_nullptr():
            future_edges.append(edge.Onext)
        if not edge.Oprev.is_nullptr():
            future_edges.append(edge.Oprev)
        if not edge.Rprev.is_nullptr():
            future_edges.append(edge.Rprev)
        if not edge.Rnext.is_nullptr():
            future_edges.append(edge.Rnext)
        if not edge.Lnext.is_nullptr():
            future_edges.append(edge.Lnext)
    '''
    edges = [(e.e[0].data, e.e[2].data) for e in QuadEdgePtr.memory.values() if not undefined_point(e.e[0].data) and not undefined_point(e.e[2].data)]
    
    return edges