import csv
import shutil
from typing import List

from tqdm import tqdm

try:
    from data import original_headers
    from helpers import chunk_list, load_csv_file
    from types_data import InputParameters
except ImportError:
    from .data import original_headers
    from .helpers import chunk_list, load_csv_file
    from .types_data import InputParameters


class CliRunner:
    def __init__(self):
        self.parameters = InputParameters()
        self.file_path = self.parameters.file_path
        self.delimiter = self.parameters.separator
        self.folder = self.file_path.parent.joinpath(
            f"{self.file_path.stem}_parsed"
        )
        self.content = load_csv_file(self.file_path)

    def split_content(self) -> List:
        return chunk_list(self.content, self.parameters.chunk_size)

    def write_files(self):
        chunks = self.split_content()
        with tqdm(
            desc="Writing files",
            unit=" file",
            total=len(chunks),
        ) as progress_bar:
            for index, chunk in enumerate(chunks):
                name = f"{self.file_path.stem}_{index}.csv"
                chunk_file = self.folder.joinpath(name)
                with open(chunk_file, mode="w", newline="") as file:
                    writer = csv.writer(file, delimiter=self.delimiter)
                    writer.writerows([original_headers, *chunk])
                progress_bar.update(1)

    def run(self):
        self.split_content()
        shutil.rmtree(self.folder, ignore_errors=True)
        self.folder.mkdir()
        self.write_files()

        print(f"Finished. Files location:\n\n{self.folder.absolute()}")


def main():
    try:
        CliRunner().run()
    except KeyboardInterrupt:
        print("Cancelling")


if __name__ == "__main__":
    main()
