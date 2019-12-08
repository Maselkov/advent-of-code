TRANSPARENT = "2"


def get_color(pixel):
    if pixel == "0":
        return '\33[30m'
    if pixel == "1":
        return '\33[37m'


def display_image(image):
    for row in image:
        for pixel in row:
            if pixel == TRANSPARENT:
                print(end=" ")
            else:
                print(get_color(pixel) + "█", end="")
        print()
    print(get_color("1"), end="")


with open("d8.txt") as f:
    image_data = f.read().strip()
WIDTH = 25
HEIGHT = 6
layers = []
pointer = 0
image = []
while pointer != len(image_data):
    for _ in range(HEIGHT):
        image.append(image_data[pointer:pointer + WIDTH])
        pointer += WIDTH
    layers.append(image)
    image = []

image = []
for _ in range(HEIGHT):
    image.append([TRANSPARENT] * WIDTH)

for layer in layers:
    for i, row in enumerate(layer):
        for j, pixel in enumerate(row):
            if image[i][j] == TRANSPARENT:
                image[i][j] = pixel

display_image(image)
