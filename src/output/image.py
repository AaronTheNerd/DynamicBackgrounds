from dataclasses import dataclass
import os

from coloring.frame import FrameDrawer
from output.directory import OutputDirectory
from point.ABCs import PointABC
from triangle.triangle import Triangle


@dataclass
class ImageFactory:
    frame_drawer: FrameDrawer

    def create(
        self,
        file_name: str,
        points: list[PointABC],
        triangles: list[Triangle],
        time: float
    ) -> None:
        output_dir = OutputDirectory()
        image = self.frame_drawer.draw(points, triangles, time)
        image.save(os.path.join(str(output_dir), file_name))
