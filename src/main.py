import json
import logging
import os

import numpy as np
from opensimplex import OpenSimplex

import point.generator.generate as generate_points
from coloring.frame import FrameDrawer
from configs import CONFIGS
from log.enable import enable_logging
from triangulation.triangulation import get_triangulation
from utils.progress_bar import progress_bar


def main():
    enable_logging()
    logger = logging.getLogger(__name__)
    output_dir = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "..", "gifs", str(CONFIGS.gif.num)
    )
    # Create directory for files if necessary
    os.system(f"mkdir -p {output_dir}")
    # Remove any existing files in directory
    os.system(f"rm {output_dir}/*")
    # Seed components
    generate_points.seed(CONFIGS.seed)
    open_simplex = OpenSimplex(CONFIGS.seed)
    # Create copy of configs to be able to remake the gif
    with open(os.path.join(output_dir, "config.json"), "w+") as file:
        json.dump(CONFIGS.dumpJSON(), file, indent=2)
    triangulation = get_triangulation(CONFIGS.triangulation)
    frame_drawer = FrameDrawer.from_json(
        CONFIGS.triangle_coloring, CONFIGS.line_coloring, CONFIGS.point_coloring
    )
    # Generate initial points
    points = generate_points.generate_points(open_simplex)
    # Generate frames
    for i, t in enumerate(
        np.linspace(0.0, 1.0, CONFIGS.gif.num_of_frames, endpoint=False)
    ):
        progress_bar(t)
        new_points = [point.at(t) for point in points]
        triangles = triangulation(new_points)
        frame = frame_drawer.draw(new_points, triangles, t)
        file_name = os.path.join(
            output_dir, f"image#{str(i).zfill(3)}.{CONFIGS.gif.file_extension}"
        )
        frame.save(file_name)
    # Convert frames to gif
    progress_bar(1.0)
    print()
    logger.info("Compiling Frames...")
    os.system(
        f"convert -delay {CONFIGS.gif.ms_per_frame} -loop 0 {output_dir}/*.{CONFIGS.gif.file_extension} -crop {CONFIGS.gif.width}x{CONFIGS.gif.height}+{CONFIGS.gif.margin}+{CONFIGS.gif.margin} +repage {output_dir}/gif{CONFIGS.gif.num}.gif"
    )
    # Remove frames
    os.system(f"rm {output_dir}/*.{CONFIGS.gif.file_extension}")


if __name__ == "__main__":
    main()
