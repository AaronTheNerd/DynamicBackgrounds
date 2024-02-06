from typing import Callable, Optional

from PIL import ImageDraw

from coloring.edge import EdgeDrawer
from coloring.triangle import TriangleDrawer
from coloring.vertex import VertexDrawer
from log.performance import measure
from point.ABCs import PointABC
from triangle import Triangle


def draw(
    image: ImageDraw.ImageDraw,
    t: float,
    points: list[PointABC],
    triangulation: Callable[[list[PointABC]], list[Triangle]],
    triangle_coloring: Optional[TriangleDrawer],
    line_coloring: Optional[EdgeDrawer],
    point_coloring: Optional[VertexDrawer],
):
    new_points = [point.at(t) for point in points]
    triangles = triangulation(new_points)
    if triangle_coloring is not None:
        draw_triangles(image, triangle_coloring, triangles, t)

    if line_coloring is not None:
        draw_lines(image, line_coloring, triangles, t)

    if point_coloring is not None:
        draw_points(image, point_coloring, new_points, t)


@measure
def draw_triangles(
    image: ImageDraw.ImageDraw,
    triangle_coloring: TriangleDrawer,
    triangles: list[Triangle],
    t: float,
) -> None:
    for triangle in triangles:
        triangle_color = triangle_coloring.get_color(triangle, t)
        image.polygon(
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
    image: ImageDraw.ImageDraw,
    line_coloring: EdgeDrawer,
    triangles: list[Triangle],
    t: float,
) -> None:
    for triangle in triangles:
        edges = triangle.edges()
        for edge in edges:
            color = line_coloring.get_color(edge, t)
            width = line_coloring.get_width(edge, t)
            image.line(
                [edge.a.x, edge.a.y, edge.b.x, edge.b.y],
                width=width,
                fill=tuple(color),
            )


@measure
def draw_points(
    image: ImageDraw.ImageDraw,
    point_coloring: VertexDrawer,
    points: list[PointABC],
    t: float,
) -> None:
    for point in points:
        color = point_coloring.get_color(point, t)
        radius = int(point_coloring.get_width(point, t) / 2)
        image.ellipse(
            [
                point.x - radius,
                point.y - radius,
                point.x + radius,
                point.y + radius,
            ],
            fill=tuple(color),
        )
