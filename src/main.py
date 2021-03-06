import json
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

import generate_points
import point
from configs import *
from get_drawing_objects import *
from triangulation import *

# Expected directory structure for gifs:
#
# DynamicBackgrounds
# +--config.json
# +--gifs
# |  +--GIF_NUM
# +--src
SRC_PATH = os.path.abspath(os.path.dirname(__file__))
GIFS_PATH = f"{SRC_PATH}/../gifs"

def draw(image, t, points, triangle_coloring, line_coloring, point_coloring):
    triangles = BowyerWatson(points, t)
    for triangle in triangles:
        triangle_color = triangle_coloring.get_color(triangle, t)
        image.polygon([triangle.a.x, triangle.a.y, triangle.b.x, triangle.b.y, triangle.c.x, triangle.c.y], fill=tuple(triangle_color))
        if LINE_DRAWING_CONFIGS["DRAW_LINES"]:
            edges = triangle.edges()
            for edge in edges:
                color = line_coloring.get_color(edge)
                width = line_coloring.get_width(edge)
                image.line([edge[0].x, edge[0].y, edge[1].x, edge[1].y], width=width, fill=tuple(color))
    if POINT_DRAWING_CONFIGS["DRAW_POINTS"]:
        for point in points:
            color = point_coloring.get_color(point.x, point.y)
            radius = int(point_coloring.get_width(point.x, point.y) / 2)
            image.ellipse([point.at(t).x - radius, point.at(t).y - radius, point.at(t).x + radius, point.at(t).y + radius], fill=tuple(color))

def run():
    # Create directory for files if necessary
    os.system(f"mkdir {GIFS_PATH}/{GIF_CONFIGS['NUM']}")
    # Remove any existing files in directory
    os.system(f"rm {GIFS_PATH}/{GIF_CONFIGS['NUM']}/*")
    # Generate random seed if necessary
    if CONFIGS["RANDOM_SEED"]:
        CONFIGS["SEED"] = random.randint(-2147483648, 2147483647)
        CONFIGS["RANDOM_SEED"] = False
    # Seed components
    generate_points.seed(CONFIGS["SEED"])
    point.seed(CONFIGS["SEED"])
    # Create copy of configs to be able to remake the gif
    with open(f"{GIFS_PATH}/{GIF_CONFIGS['NUM']}/config.json", 'w+') as file:
        json.dump(CONFIGS, file, indent=4)
    # Generate objects needed to color the gif
    triangle_coloring = get_triangle_coloring_object()
    line_coloring = get_line_drawing_object()
    point_coloring = get_point_drawing_object()
    # Generate initial points
    points = generate_points.generate_points()
    # Generate frames
    i = 0
    for t in np.linspace(0.0, 1.0, CONFIGS["NUM_OF_FRAMES"], endpoint=False):
        image = Image.new("RGB", (WIDTH, HEIGHT), tuple(CONFIGS["BACKGROUND_COLOR"]))
        image_draw = ImageDraw.Draw(image)
        draw(image_draw, t, points, triangle_coloring, line_coloring, point_coloring)
        file_name = f"{GIFS_PATH}/{GIF_CONFIGS['NUM']}/image#{str(i).zfill(3)}.bmp"
        image.save(file_name)
        i += 1
    # Convert frames to gif
    os.system(f"convert -delay {GIF_CONFIGS['MS_PER_FRAME']} -loop 0 {GIFS_PATH}/{GIF_CONFIGS['NUM']}/*.bmp -crop {CONFIGS['WIDTH']}x{CONFIGS['HEIGHT']}+{GIF_CONFIGS['MARGIN']}+{GIF_CONFIGS['MARGIN']} +repage {GIFS_PATH}/{GIF_CONFIGS['NUM']}/gif{GIF_CONFIGS['NUM']}.gif")
    # Remove frames
    os.system(f"rm {GIFS_PATH}/{GIF_CONFIGS['NUM']}/*.bmp")

if __name__ == "__main__":
    run()
