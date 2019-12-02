def get_fuel(fuel):
    fuel = ((fuel // 3) - 2)
    if fuel <= 0:
        return 0
    return fuel + get_fuel(fuel)


total = 0
with open("d1.txt", "r") as f:
    for line in f:
        total += get_fuel(int(line))

print(total)
