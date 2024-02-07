import json
import logging
import os

import numpy as np
from opensimplex import OpenSimplex
from log.performance import measure

import point.generator.generate as generate_points
from coloring.frame import FrameDrawer
from configs import CONFIGS
from log.enable import enable_logging
from output_directory import OutputDirectory
from triangulation.triangulation import get_triangulation
from utils.progress_bar import progress_bar


def main():
    enable_logging()
    logger = logging.getLogger(__name__)

    output_dir = OutputDirectory()
    output_dir.create_empty_directory()

    dump_configs(output_dir)    
    create_frames(output_dir)
    logger.info("Compiling Frames...")
    compile_frames(output_dir)
    
    output_dir.clear_files(CONFIGS.gif.file_extension)


def dump_configs(output_dir: OutputDirectory) -> None:
    with open(os.path.join(str(output_dir), "config.json"), "w+") as file:
        json.dump(CONFIGS.dumpJSON(), file, indent=2)


def create_frames(output_dir: OutputDirectory) -> None:
    frame_drawer = FrameDrawer.from_json(
        CONFIGS.triangle_coloring, CONFIGS.line_coloring, CONFIGS.point_coloring
    )
    algorithm = get_triangulation(CONFIGS.triangulation)
    points = generate_points.generate_points()
    for frame_index, time in enumerate_frames(CONFIGS.gif.num_of_frames):
        progress_bar(time)
        new_points = [point.at(time) for point in points]
        triangles = algorithm(new_points)
        frame = frame_drawer.draw(new_points, triangles, time)
        file_name = os.path.join(
            str(output_dir),
            f"image#{str(frame_index).zfill(3)}.{CONFIGS.gif.file_extension}",
        )
        frame = frame.crop((
            CONFIGS.gif.margin,
            CONFIGS.gif.margin,
            CONFIGS.gif.margin + CONFIGS.gif.width,
            CONFIGS.gif.margin + CONFIGS.gif.height,
        ))
        frame.save(file_name)
    # Convert frames to gif
    progress_bar(1.0)
    print()


def enumerate_frames(num_frames: int) -> enumerate:
    return enumerate(np.linspace(0.0, 1.0, num_frames, endpoint=False))

@measure
def compile_frames(output_dir: OutputDirectory) -> None:
    os.system(
        f"convert -delay {CONFIGS.gif.ms_per_frame} -loop 0 {output_dir}/*.{CONFIGS.gif.file_extension} +repage {output_dir}/gif{CONFIGS.gif.num}.gif"
    )

if __name__ == "__main__":
    main()
