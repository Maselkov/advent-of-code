with open("d8.txt") as f:
    image_data = f.read().strip()
WIDTH = 25
HEIGHT = 6

layers = []
image = []
pointer = 0
while pointer != len(image_data):
    for _ in range(HEIGHT):
        image.append(image_data[pointer:pointer + WIDTH])
        pointer += WIDTH
    layers.append(image)
    image = []


def digit_count(layer, digit):
    digit = str(digit)
    c = 0
    for row in layer:
        for pixel in row:
            if pixel == digit:
                c += 1
    return c


sought = 0
layer_with_least = []
lowest_count = float("inf")
for layer in layers:
    count = digit_count(layer, sought)
    if count < lowest_count:
        layer_with_least = layer
        lowest_count = count

print(digit_count(layer_with_least, 1) * digit_count(layer_with_least, 2))
