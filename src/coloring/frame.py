from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from PIL import Image, ImageDraw

from coloring.edge import EdgeDrawer
from coloring.triangle import TriangleDrawer
from coloring.vertex import VertexDrawer
from configs import CONFIGS
from log.performance import measure
from point.ABCs import PointABC
from serial.ABCs import SerialABC
from serial.JSON_types import JSON_object
from triangle.triangle import Triangle


@dataclass
class FrameDrawer(SerialABC):
    triangle_drawer: Optional[TriangleDrawer]
    edge_drawer: Optional[EdgeDrawer]
    vertex_drawer: Optional[VertexDrawer]

    @classmethod
    def from_json(
        cls,
        triangle_coloring: JSON_object,
        line_coloring: JSON_object,
        point_coloring: JSON_object,
    ) -> FrameDrawer:
        triangle_drawer = None
        if triangle_coloring is not None:
            triangle_drawer = TriangleDrawer.from_json(**triangle_coloring)
        edge_drawer = None
        if line_coloring is not None:
            edge_drawer = EdgeDrawer.from_json(**line_coloring)
        vertex_drawer = None
        if point_coloring is not None:
            vertex_drawer = VertexDrawer.from_json(**point_coloring)
        return cls(triangle_drawer, edge_drawer, vertex_drawer)

    def draw(
        self,
        points: list[PointABC],
        triangles: list[Triangle],
        time: float,
    ) -> Image.Image:
        frame = Image.new(
            "RGB",
            (CONFIGS.full_width, CONFIGS.full_height),
            tuple(CONFIGS.output.background_color),
        )
        frame_draw = ImageDraw.Draw(frame)
        if self.triangle_drawer is not None:
            self.draw_triangles(frame_draw, triangles, time)
        if self.edge_drawer is not None:
            self.draw_lines(frame_draw, triangles, time)
        if self.vertex_drawer is not None:
            self.draw_points(frame_draw, points, time)
        return frame

    @measure
    def draw_triangles(
        self,
        frame_draw: ImageDraw.ImageDraw,
        triangles: list[Triangle],
        time: float,
    ) -> None:
        for triangle in triangles:
            triangle_color = self.triangle_drawer.get_color(triangle, time)
            frame_draw.polygon(
                [
                    triangle.a.x,
                    triangle.a.y,
                    triangle.b.x,
                    triangle.b.y,
                    triangle.c.x,
                    triangle.c.y,
                ],
                fill=tuple(triangle_color),
            )

    @measure
    def draw_lines(
        self, frame_draw: ImageDraw.ImageDraw, triangles: list[Triangle], time: float
    ) -> None:
        for triangle in triangles:
            edges = triangle.edges()
            for edge in edges:
                color = self.edge_drawer.get_color(edge, time)
                width = self.edge_drawer.get_width(edge, time)
                frame_draw.line(
                    [edge.a.x, edge.a.y, edge.b.x, edge.b.y],
                    width=width,
                    fill=tuple(color),
                )

    @measure
    def draw_points(
        self, frame_draw: ImageDraw.ImageDraw, points: list[PointABC], time: float
    ) -> None:
        for point in points:
            color = self.vertex_drawer.get_color(point, time)
            radius = int(self.vertex_drawer.get_width(point, time) / 2)
            frame_draw.ellipse(
                [
                    point.x - radius,
                    point.y - radius,
                    point.x + radius,
                    point.y + radius,
                ],
                fill=tuple(color),
            )
