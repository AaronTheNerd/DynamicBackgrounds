import os
from dataclasses import dataclass, field

from configs import CONFIGS


@dataclass
class OutputDirectory:
    directory: str = field(init=False)

    def __post_init__(self) -> None:
        self.directory = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "..",
            "gifs",
            str(CONFIGS.gif.num),
        )

    def __str__(self) -> str:
        return self.directory

    def __repr__(self) -> str:
        return self.directory

    def create_empty_directory(self) -> None:
        os.system(f"mkdir -p {self.directory}")
        os.system(f"rm {self.directory}/*")

    def clear_files(self, file_extension: str) -> None:
        os.system(f"rm {self.directory}/*.{file_extension}")
