from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.validator import PathValidator, EmptyInputValidator

try:
    from src.config import DEBUG
except ImportError:
    from .config import DEBUG


class InputParameters:
    file_path: Path
    chunk_size: int
    separator: str

    def __init__(self):
        self.load_file_path()
        self.load_chunk_size()
        self.load_separator()

    def load_file_path(self):
        if DEBUG:
            file_name = Path(__file__).parent.parent.joinpath(
                "rpls2023idf_xy.csv"
            )
        else:
            file_name = inquirer.filepath(
                message="Enter file to upload:",
                default=str(Path.home()),
                validate=PathValidator(
                    is_file=True, message="Input is not a file"
                ),
                only_files=True,
            ).execute()
        self.file_path = Path(file_name)

    def load_chunk_size(self):
        if DEBUG:
            chunk_size = 100000
        else:
            chunk_size = inquirer.number(
                message="Enter chunk size:",
                min_allowed=1,
                default=100000,
                validate=EmptyInputValidator(),
            ).execute()
        self.chunk_size = int(chunk_size)

    def load_separator(self):
        if DEBUG:
            self.separator = ","
        else:
            self.separator = inquirer.text(
                message="Separator:", default=","
            ).execute()
