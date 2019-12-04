import math


def det(a, b, c, d):
    return a * d - b * c


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lies_on(self, segment):
        return Segment(segment.a, self).length + Segment(
            segment.b, self).length == segment.length


class Segment:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.length = math.sqrt(((a.x - b.x)**2) + ((a.y - b.y)**2))

    def find_intersection(self, other):
        # We look for the point of intersection between the two lines
        # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
        x1mx2 = self.a.x - self.b.x
        y3my4 = other.a.y - other.b.y
        y1my2 = self.a.y - self.b.y
        x3mx4 = other.a.x - other.b.x
        denom = det(x1mx2, y1my2, x3mx4, y3my4)
        if denom == 0:
            return None
        det_l = det(self.a.x, self.a.y, self.b.x, self.b.y)
        det_r = det(other.a.x, other.a.y, other.b.x, other.b.y)
        new_x = det(det_l, x1mx2, det_r, x3mx4) / denom
        new_y = det(det_l, y1my2, det_r, y3my4) / denom
        if not new_x and not new_y:
            return None
        point = Point(new_x, new_y)
        # Making sure it within both the segments
        if not point.lies_on(self):
            return None
        if not point.lies_on(other):
            return None
        return Point(new_x, new_y)


def manhattan_distance(a, b):
    return int(abs(a.x - b.x) + abs(a.y - b.y))


wires = []
with open("d3.txt", "r") as f:
    for line in f:
        current_pos = Point(0, 0)
        segments = []
        movements = line.split(",")
        for movement in movements:
            direction = movement[0]
            amount = int(movement[1:])
            if direction == "R":
                new_pos = (current_pos.x + amount, current_pos.y)
            if direction == "L":
                new_pos = (current_pos.x - amount, current_pos.y)
            if direction == "U":
                new_pos = (current_pos.x, current_pos.y + amount)
            if direction == "D":
                new_pos = (current_pos.x, current_pos.y - amount)
            new_pos = Point(*new_pos)
            segments.append(Segment(current_pos, new_pos))
            current_pos = new_pos
        wires.append(segments)
    dist = float("inf")
    for segment_1 in wires[0]:
        for segment_2 in wires[1]:
            intersection = segment_1.find_intersection(segment_2)
            if intersection:
                new_dist = manhattan_distance(Point(0, 0), intersection)
                if new_dist < dist:
                    dist = new_dist
print(dist)
