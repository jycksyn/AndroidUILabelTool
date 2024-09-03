import argparse
from pathlib import Path
from tap import Tap

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)

    p = parser.parse_args()
    if not (p.file_path.is_dir() and p.file_path.exists()):
        raise ValueError(f"Folder {p.file_path} does not exist")

    xml_files = p.file_path.glob("*.xml")
    for filename in xml_files:
        print(filename)

    