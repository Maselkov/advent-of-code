import sys

data = []

# The default recursion limit is too low for us
# This is probably an extremally inelegant solution. Oh well.

sys.setrecursionlimit(10000000)
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

    def __repr__(self):
        children = ", ".join(c.name for c in self.children)
        return f"Name:{self.name} Children: ({children})"

    def count_orbits(self, depth=0):
        total = 0
        for child in self.children:
            total += child.count_orbits(depth + 1)
        return depth + total


with open("d6.txt") as f:
    for line in f:
        data.append(line.strip().split(")"))

for obj in data:
    if obj[0] == ROOT_NAME:
        root = Body(obj[0])
print(root.count_orbits())
