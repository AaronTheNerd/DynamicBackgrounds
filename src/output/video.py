import logging
import os
from dataclasses import dataclass
from typing import Callable

import cv2
import numpy as np

from configs import CONFIGS
from log.performance import measure
from output.directory import OutputDirectory
from output.image import ImageFactory
from point.ABCs import PointABC
from triangle.triangle import Triangle
from utils.progress_bar import progress_bar


@dataclass
class VideoFactory:
    frame_factory: ImageFactory

    def create(
        self,
        file_name: str,
        points: list[PointABC],
        algorithm: Callable[[list[PointABC]], list[Triangle]],
    ) -> None:
        frame_names = self._create_frames(points, algorithm)
        self._compile(file_name, frame_names)
        output_dir = OutputDirectory()
        output_dir.clear_files(frame_names)

    def _create_frames(
        self,
        points: list[PointABC],
        algorithm: Callable[[list[PointABC]], list[Triangle]],
    ) -> list[str]:
        frame_names = []
        for frame_index, time in self._enumerate_frames(
            CONFIGS.output.video.num_of_frames
        ):
            progress_bar(time)
            new_points = [point.at(time) for point in points]
            triangles = algorithm(new_points)
            frame_name = f"frame#{str(frame_index).zfill(3)}.{CONFIGS.output.video.frame_file_extension}"
            self.frame_factory.create(frame_name, new_points, triangles, time)
            frame_names.append(frame_name)
        progress_bar(1.0)
        print()
        return frame_names

    def _enumerate_frames(self, num_frames: int) -> enumerate:
        return enumerate(np.linspace(0.0, 1.0, num_frames, endpoint=False))

    @measure
    def _compile(self, file_name: str, frame_names: list[str]) -> None:
        logger = logging.getLogger(__name__)
        logger.info("Began Compiling Frames")
        output_dir = OutputDirectory()
        video_name = os.path.join(str(output_dir), file_name)
        video = cv2.VideoWriter(
            video_name,
            0,
            CONFIGS.output.video.framerate,
            (CONFIGS.output.width, CONFIGS.output.height),
        )
        try:
            for frame_name in frame_names:
                frame = cv2.imread(os.path.join(str(output_dir), frame_name))
                video.write(frame)
        finally:
            cv2.destroyAllWindows()
            video.release()
            logger.info("Finished Compiling Frames")
