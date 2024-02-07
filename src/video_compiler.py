import logging
import os

import cv2

from configs import CONFIGS
from log.performance import measure
from output_directory import OutputDirectory


@measure
def compile_frames(output_dir: OutputDirectory) -> None:
    logger = logging.getLogger(__name__)
    logger.info("Began Compiling Frames")
    image_names = sorted(
        [
            image
            for image in os.listdir(str(output_dir))
            if image.endswith(CONFIGS.output.frame_file_extension)
        ]
    )
    video_name = os.path.join(str(output_dir), f"video{CONFIGS.output.num}.avi")
    video = cv2.VideoWriter(
        video_name,
        0,
        CONFIGS.output.framerate,
        (CONFIGS.output.width, CONFIGS.output.height),
    )
    try:
        for image_name in image_names:
            image = cv2.imread(os.path.join(str(output_dir), image_name))
            video.write(image)
    finally:
        cv2.destroyAllWindows()
        video.release()
        logger.info("Finished Compiling Frames")
