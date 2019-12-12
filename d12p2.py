from os import path
import re
import copy
import itertools
import math


def lcm(numbers):
    res = numbers[0]
    for i in numbers[1:]:
        res = res * i // math.gcd(res, i)
    return res


class Moon:
    def __init__(self, coords):
        self.position = coords
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]
        self.velocity = [0, 0, 0]

    def energy(self):
        return sum(abs(x) for x in self.position) * sum(
            abs(x) for x in self.velocity)


moons = []

with open(f"{path.basename(__file__).split('p')[0]}.txt") as f:
    for line in f:
        line = re.sub("[>=<,]", "", line)
        coords = [int(coord[1:]) for coord in line.split()]
        moons.append(Moon(coords))

initial = copy.deepcopy(moons)
steps = []
for i in range(3):
    j = 0
    while True:
        j += 1
        for moon_1, moon_2 in itertools.combinations(moons, 2):
            if moon_1.position[i] > moon_2.position[i]:
                moon_1.velocity[i] -= 1
                moon_2.velocity[i] += 1
            elif moon_1.position[i] < moon_2.position[i]:
                moon_1.velocity[i] += 1
                moon_2.velocity[i] -= 1
        for moon in moons:
            moon.position[i] += moon.velocity[i]
        for moon, old in zip(moons, initial):
            if moon.position[i] != old.position[i] or moon.velocity[
                    i] != 0 or j <= 1:
                break
        else:
            steps.append(j)
            break
print(steps)
print(lcm(steps))
