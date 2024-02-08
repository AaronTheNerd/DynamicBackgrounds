import json
import os
from typing import Callable

import point.generator.generate as generate_points
from coloring.frame import FrameDrawer
from configs import CONFIGS
from log.enable import enable_logging
from output.directory import OutputDirectory
from output.image import ImageFactory
from output.video import VideoFactory
from point.ABCs import PointABC
from triangle.triangle import Triangle
from triangulation.triangulation import get_triangulation


def main():
    enable_logging()
    output_dir = OutputDirectory()
    output_dir.create_empty_directory()
    dump_configs()
    create_outputs()


def dump_configs() -> None:
    output_dir = OutputDirectory()
    with open(os.path.join(str(output_dir), "config.json"), "w+") as file:
        json.dump(CONFIGS.dumpJSON(), file, indent=2)


def create_outputs() -> None:
    algorithm = get_triangulation(CONFIGS.triangulation)
    points = generate_points.generate_points()
    frame_drawer = FrameDrawer.from_json(
        CONFIGS.triangle_coloring, CONFIGS.line_coloring, CONFIGS.point_coloring
    )
    image_factory = ImageFactory(frame_drawer)
    if CONFIGS.output.image is not None:
        create_image(image_factory, points, algorithm)
    if CONFIGS.output.video is not None:
        create_video(image_factory, points, algorithm)


def create_image(
    image_factory: ImageFactory,
    points: list[PointABC],
    algorithm: Callable[[list[PointABC]], list[Triangle]],
) -> None:
    new_points = [point.at(0) for point in points]
    triangles = algorithm(new_points)
    image_factory.create(
        f"image.{CONFIGS.output.image.file_extension}", new_points, triangles, 0
    )


def create_video(
    image_factory: ImageFactory,
    points: list[PointABC],
    algorithm: Callable[[list[PointABC]], list[Triangle]],
):
    video_factory = VideoFactory(image_factory)
    video_factory.create("video.avi", points, algorithm)


if __name__ == "__main__":
    main()
