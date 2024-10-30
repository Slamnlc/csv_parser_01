import csv
from pathlib import Path
from typing import List

from tqdm import tqdm

try:
    from data import nbpiece_codes, accessibility_codes, priority_urban_area
except ImportError:
    from .data import nbpiece_codes, accessibility_codes, priority_urban_area


def chunk_list(lst: list, chunk_size: int):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def load_csv_file(file_path: Path) -> List[List[str]]:
    print("Loading file...")
    content = []
    with open(file_path, mode="r") as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)[0].split(";")
        headers_count = len(headers)
        rows = [_row for _row in csv_reader]
        with tqdm(
            desc=f"Parsing file {file.name}", unit=" rows", total=len(rows)
        ) as progress_bar:
            for row in rows:
                full_row = ",".join(row).split(";")[:headers_count]
                extend_1 = full_row[20].split(",")
                extend_2 = full_row[21].split(",")
                full_row = full_row[: len(full_row) - 4]
                full_row.extend(extend_1 + extend_2)
                priority_urban = priority_urban_area[full_row[8]]
                nbpiece = full_row[9]
                if nbpiece.isdigit():
                    nbpiece = int(nbpiece)
                nbpiece_text = nbpiece_codes[nbpiece]
                accessibility_for_disabled = accessibility_codes[
                    int(full_row[14])
                ]
                full_row[8] = priority_urban
                full_row[9] = nbpiece_text
                full_row[14] = accessibility_for_disabled
                progress_bar.update(1)
                content.append(full_row)
    return content
