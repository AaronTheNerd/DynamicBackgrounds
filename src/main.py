import json
import os
from typing import Optional

import numpy as np
from opensimplex import OpenSimplex
from PIL import Image, ImageDraw

import point.generator.generate as generate_points
from point.ABCs import PointABC
from bowyer_watson import BowyerWatson
from coloring.triangle.ABCs import TriangleDrawerABC
from coloring.line.ABCs import LineDrawerABC
from coloring.point.ABCs import PointDrawerABC
from coloring.line.line import get_line_object
from coloring.point.point import get_point_object
from coloring.triangle.triangle import get_triangle_object
from configs import CONFIGS
from utils.progress_bar import progress_bar

SRC_PATH = os.path.abspath(os.path.dirname(__file__))
GIFS_PATH = f"{SRC_PATH}/../gifs"


def draw(
    image,
    t: float,
    points: list[PointABC],
    triangle_coloring: Optional[TriangleDrawerABC],
    line_coloring: Optional[LineDrawerABC],
    point_coloring: Optional[PointDrawerABC],
):
    new_points = [point.at(t) for point in points]
    triangles = BowyerWatson(new_points)
    if triangle_coloring is not None:
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
    if line_coloring is not None:
        for triangle in triangles:
            edges = triangle.edges()
            for edge in edges:
                color = line_coloring.get_color(edge, t)
                width = line_coloring.get_width(edge, t)
                image.line([edge.a.x, edge.a.y, edge.b.x, edge.b.y], width=width, fill=tuple(color))
    if point_coloring is not None:
        for point in new_points:
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
    # Create directory for files if necessary
    os.system(f"mkdir -p {GIFS_PATH}/{CONFIGS.gif_configs.num}")
    # Remove any existing files in directory
    os.system(f"rm {GIFS_PATH}/{CONFIGS.gif_configs.num}/*")
    # Seed components
    generate_points.seed(CONFIGS.seed)
    open_simplex = OpenSimplex(CONFIGS.seed)
    # Create copy of configs to be able to remake the gif
    with open(f"{GIFS_PATH}/{CONFIGS.gif_configs.num}/config.json", "w+") as file:
        json.dump(CONFIGS.dumpJSON(), file, indent=4)
    # Generate objects needed to color the gif
    triangle_coloring = None
    if CONFIGS.triangle_coloring:
        triangle_coloring = get_triangle_object(CONFIGS.triangle_coloring)
    line_coloring = None
    if CONFIGS.line_coloring:
        line_coloring = get_line_object(CONFIGS.line_coloring)
    point_coloring = None
    if CONFIGS.point_coloring:
        point_coloring = get_point_object(CONFIGS.point_coloring)
    # Generate initial points
    points = generate_points.generate_points(open_simplex)
    # Generate frames
    for i, t in enumerate(np.linspace(0.0, 1.0, CONFIGS.gif_configs.num_of_frames, endpoint=False)):
        image = Image.new(
            "RGB",
            (CONFIGS.full_width, CONFIGS.full_height),
            tuple(CONFIGS.gif_configs.background_color),
        )
        image_draw = ImageDraw.Draw(image)
        progress_bar(t)
        draw(image_draw, t, points, triangle_coloring, line_coloring, point_coloring)
        file_name = f"{GIFS_PATH}/{CONFIGS.gif_configs.num}/image#{str(i).zfill(3)}.{CONFIGS.gif_configs.file_extension}"
        image.save(file_name)
    # Convert frames to gif
    progress_bar(1.0)
    print("\nCompiling Frames...")
    os.system(
        f"convert -delay {CONFIGS.gif_configs.ms_per_frame} -loop 0 {GIFS_PATH}/{CONFIGS.gif_configs.num}/*.{CONFIGS.gif_configs.file_extension} -crop {CONFIGS.gif_configs.width}x{CONFIGS.gif_configs.height}+{CONFIGS.gif_configs.margin}+{CONFIGS.gif_configs.margin} +repage {GIFS_PATH}/{CONFIGS.gif_configs.num}/gif{CONFIGS.gif_configs.num}.gif"
    )
    # Remove frames
    os.system(f"rm {GIFS_PATH}/{CONFIGS.gif_configs.num}/*.{CONFIGS.gif_configs.file_extension}")


if __name__ == "__main__":
    run()
