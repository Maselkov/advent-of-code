from os import path
import re
import itertools


class Moon:
    def __init__(self, coords):
        self.position = coords
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

for step in range(1000):
    for moon_1, moon_2 in itertools.combinations(moons, 2):
        for i in range(3):
            if moon_1.position[i] > moon_2.position[i]:
                moon_1.velocity[i] -= 1
                moon_2.velocity[i] += 1
            elif moon_1.position[i] < moon_2.position[i]:
                moon_1.velocity[i] += 1
                moon_2.velocity[i] -= 1
    for moon in moons:
        for i in range(3):
            moon.position[i] += moon.velocity[i]

energy_sum = sum(moon.energy() for moon in moons)
print(energy_sum)
