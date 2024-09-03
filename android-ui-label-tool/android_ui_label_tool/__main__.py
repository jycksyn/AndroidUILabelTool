from pathlib import Path
from tap import Tap
import xml.etree.ElementTree as ET 

class Args(Tap):
    file_path: Path = Path.cwd()

def find_leaves(node: ET.Element):
    children = [*node.findall('*')]
    if len(children) == 0:
        return [node]
    leaves: list[ET.Element] = []
    for child in children:
        leaves.extend(find_leaves(child))
    return leaves


def process_xml(xml_file: Path):
    png_file = xml_file.with_suffix(".png")
    if not png_file.exists():
        raise ValueError(f"Corresponding PNG file {png_file} does not exist")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    leaves = find_leaves(root)
    for leaf in leaves:
        print(leaf.tag, leaf.get('bounds'))
    

if __name__ == "__main__":
    parser = Args()

    p = parser.parse_args()
    if not (p.file_path.is_dir() and p.file_path.exists()):
        raise ValueError(f"Folder {p.file_path} does not exist")

    xml_files = p.file_path.glob("*.xml")
    for filename in xml_files:
        xml_file = p.file_path / filename
        try:
            process_xml(xml_file)
        except Exception as e:
            print(f"Error processing {xml_file}: {e}")

    