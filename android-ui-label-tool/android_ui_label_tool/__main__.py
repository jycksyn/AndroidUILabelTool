from pathlib import Path
from tap import Tap
import xml.etree.ElementTree as ET 
import re
from PIL import Image, ImageDraw

bounds_pattern = re.compile(r'\[(?P<left>\d+),(?P<top>\d+)\]\[(?P<right>\d+),(?P<bottom>\d+)\]')

class Bounds:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        
    @staticmethod
    def from_node(node: ET.Element) -> 'Bounds | None':
        bounds: str = node.get('bounds') #type: ignore
        match = bounds_pattern.match(bounds)
        if match is None:
            return None
        left, top, right, bottom = map(int, match.groups())
        return Bounds(left, top, right, bottom)
    
    def to_list(self) -> list[int]:
        return [self.left, self.top, self.right, self.bottom]

class Args(Tap):
    input_dir: Path = Path.cwd()
    output_dir: Path = input_dir
    overwrite: bool = False

def find_leaves(node: ET.Element) -> list[ET.Element]:
    children = [*node.findall('*')]
    if len(children) == 0:
        return [node]
    leaves: list[ET.Element] = []
    for child in children:
        leaves.extend(find_leaves(child))
    return leaves

def add_annotations(bounds: list[Bounds], im: Image.Image):
    draw = ImageDraw.Draw(im)
    for bound in bounds:
        draw.rectangle(bound.to_list(), outline='yellow', width=5)

def process_xml(xml_file: Path, output_dir: Path, overwrite: bool):
    png_file = xml_file.with_suffix(".png")
    if not png_file.exists():
        raise ValueError(f"Corresponding PNG file {png_file} does not exist")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    leaves = find_leaves(root)
    bounds = [Bounds.from_node(node) for node in leaves if node.tag == 'node']
    bounds = [b for b in bounds if b is not None]

    with Image.open(png_file) as im:
        add_annotations(bounds, im)
        output_file = output_dir / (xml_file.stem + "_highlighted.png")
        if output_file.exists() and not overwrite:
            raise ValueError(f"Output file {output_file} already exists")
        im.save(output_file, "PNG")

def validate_args(p: Args):
    if not (p.input_dir.is_dir() and p.input_dir.exists()):
        raise ValueError(f"Folder {p.input_dir} does not exist")
    
    if not (p.output_dir.is_dir() and p.output_dir.exists()):
        raise ValueError(f"Output folder {p.output_dir} does not exist")
    

if __name__ == "__main__":
    parser = Args()

    p = parser.parse_args()

    try:
        validate_args(p)
        xml_files = p.input_dir.glob("*.xml")
        for xml_file in xml_files:
            try:
                process_xml(xml_file, p.output_dir, p.overwrite)
            except Exception as e:
                print(f"Error processing {xml_file}: {e}")
    except Exception as e:
        print(f"Error: {e}")

    