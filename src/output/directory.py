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
            "..",
            "output",
            str(CONFIGS.output.name),
        )

    def __str__(self) -> str:
        return self.directory

    def __repr__(self) -> str:
        return self.directory

    def create_empty_directory(self) -> None:
        os.system(f"mkdir -p {self.directory}")
        os.system(f"rm {self.directory}/*")

    def clear_files(self, file_names: list[str]) -> None:
        for file_name in file_names:
            os.remove(os.path.join(self.directory, file_name))
