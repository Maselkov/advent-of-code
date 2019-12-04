number_range = range(108457, 562041)

count = 0


def meets_criteria(number):
    string = str(number)
    current_digit = int(string[0])
    for c in map(int, string[1:]):
        if c < current_digit:
            return False
        current_digit = c
    current_character = string[0]
    repeats = 0
    has_double = False
    for c in string[1:]:
        if c == current_character:
            repeats += 1
        elif repeats == 1:
            has_double = True
            break
        else:
            repeats = 0
        if repeats > 1:
            has_double = False
        current_character = c
    # In case the two digits are at the end
    if repeats == 1:
        has_double = True
    return has_double


for i in number_range:
    if meets_criteria(i):
        count += 1
print(count)
