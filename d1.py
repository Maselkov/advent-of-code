total = 0
with open("d1.txt", "r") as f:
    for line in f:
        fuel = int(line)
        total += (fuel // 3) - 2

print(total)
