from xml.etree import ElementTree
from pprint import pprint


def print_tree(file_name):
    with open(file_name, 'rt') as f:
        tree = ElementTree.parse(f)

    for node in tree.getroot()[5]:
        print(node.tag)


if __name__ == '__main__':
    print_tree('Web.xml')
