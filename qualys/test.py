import xml.etree.ElementTree as ET
from pprint import pprint


def main(filename):
    """
    """
    tree = ET.parse(filename)
    root = tree.getroot()
    result = []
    for tag in root:
        print(tag.tag, tag.text)


if __name__ == '__main__':
    main('1.xml')
