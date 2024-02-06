import json
import logging
import os
from typing import Callable, Optional

import numpy as np
from opensimplex import OpenSimplex
from PIL import Image, ImageDraw

import point.generator.generate as generate_points
from coloring.edge import EdgeDrawer
from coloring.triangle import TriangleDrawer
from coloring.vertex import VertexDrawer
from configs import CONFIGS
from log.enable import enable_logging
from log.performance import measure
from point.ABCs import PointABC
from triangle import Edge, Triangle
from triangulation.triangulation import get_triangulation
from utils.progress_bar import progress_bar

SRC_PATH = os.path.abspath(os.path.dirname(__file__))
GIFS_PATH = f"{SRC_PATH}/../gifs"


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


def run():
    enable_logging()
    logger = logging.getLogger(__name__)
    # Create directory for files if necessary
    os.system(f"mkdir -p {GIFS_PATH}/{CONFIGS.gif.num}")
    # Remove any existing files in directory
    os.system(f"rm {GIFS_PATH}/{CONFIGS.gif.num}/*")
    # Seed components
    generate_points.seed(CONFIGS.seed)
    open_simplex = OpenSimplex(CONFIGS.seed)
    # Create copy of configs to be able to remake the gif
    with open(f"{GIFS_PATH}/{CONFIGS.gif.num}/config.json", "w+") as file:
        json.dump(CONFIGS.dumpJSON(), file, indent=4)
    triangulation = get_triangulation(CONFIGS.triangulation)
    # Generate objects needed to color the gif
    triangle_coloring = None
    if CONFIGS.triangle_coloring:
        triangle_coloring = TriangleDrawer.from_json(**CONFIGS.triangle_coloring)
    line_coloring = None
    if CONFIGS.line_coloring:
        line_coloring = EdgeDrawer.from_json(**CONFIGS.line_coloring)
    point_coloring = None
    if CONFIGS.point_coloring:
        point_coloring = VertexDrawer.from_json(**CONFIGS.point_coloring)
    # Generate initial points
    points = generate_points.generate_points(open_simplex)
    # Generate frames
    for i, t in enumerate(
        np.linspace(0.0, 1.0, CONFIGS.gif.num_of_frames, endpoint=False)
    ):
        image = Image.new(
            "RGB",
            (CONFIGS.full_width, CONFIGS.full_height),
            tuple(CONFIGS.gif.background_color),
        )
        image_draw = ImageDraw.Draw(image)
        progress_bar(t)
        draw(
            image_draw,
            t,
            points,
            triangulation,
            triangle_coloring,
            line_coloring,
            point_coloring,
        )
        file_name = f"{GIFS_PATH}/{CONFIGS.gif.num}/image#{str(i).zfill(3)}.{CONFIGS.gif.file_extension}"
        image.save(file_name)
    # Convert frames to gif
    progress_bar(1.0)
    print()
    logger.info("Compiling Frames...")
    os.system(
        f"convert -delay {CONFIGS.gif.ms_per_frame} -loop 0 {GIFS_PATH}/{CONFIGS.gif.num}/*.{CONFIGS.gif.file_extension} -crop {CONFIGS.gif.width}x{CONFIGS.gif.height}+{CONFIGS.gif.margin}+{CONFIGS.gif.margin} +repage {GIFS_PATH}/{CONFIGS.gif.num}/gif{CONFIGS.gif.num}.gif"
    )
    # Remove frames
    os.system(f"rm {GIFS_PATH}/{CONFIGS.gif.num}/*.{CONFIGS.gif.file_extension}")


if __name__ == "__main__":
    run()
