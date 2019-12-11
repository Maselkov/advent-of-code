from os import path
import math

def angle(p1, p2):
    return math.atan2(p1[1] - p2[1], p1[0] - p2[0])


asteroids = []
with open(f"{path.basename(__file__).split('p')[0]}.txt") as f:
    for y, line in enumerate(f):
        for x, position in enumerate(line):
            if position == "#":
                asteroids.append((x, y))


def count_visible_asteroids(position):
    count = 0
    angles = []
    for asteroid in asteroids:
        an = angle(position, asteroid)
        if an in angles:
            continue
        count += 1
        angles.append(an)
    return count


most_count = 0
for pos in asteroids:
    c = count_visible_asteroids(pos)
    if c > most_count:
        most_count = c
print(most_count)
