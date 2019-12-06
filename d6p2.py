import sys

data = []

# Default recursion limit is too low for us
# This is probably an extremally inelegant solution. Oh well.

sys.setrecursionlimit(10**4)
ROOT_NAME = "COM"


def find_children(identifier):
    children = []
    for parent, child in data:
        if parent == identifier:
            children.append(Body(child))
    return children


class Body:
    def __init__(self, name):
        self.name = name
        self.children = find_children(name)

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        children = ", ".join(c.name for c in self.children)
        return f"Name:{self.name} Children: ({children})"

    def count_orbits(self, depth=0):
        total = 0
        for child in self.children:
            total += child.count_orbits(depth + 1)
        return depth + total

    def seek_body(self, name):
        stack = []

        def seek(node):
            if node.name == name:
                return True
            for child in node.children:
                if seek(child):
                    stack.append(node.name)
                    return True
            return False

        seek(self)
        return stack


def calculate_transfers(path_1, path_2):
    return distance_to_common(path_1, path_2) + distance_to_common(
        path_2, path_1)


def distance_to_common(path_1, path_2):
    for i, item in enumerate(path_1):
        if item in path_2:
            return i


with open("d6.txt") as f:
    for line in f:
        data.append(line.strip().split(")"))

for obj in data:
    if obj[0] == ROOT_NAME:
        root = Body(obj[0])
you_path = root.seek_body("YOU")
san_path = root.seek_body("SAN")
print(calculate_transfers(you_path, san_path))
