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
    for c in string[1:]:
        if c == current_character:
            break
        current_character = c
    else:  # The loop didn't break so no double
        return False
    return True


for i in number_range:
    if meets_criteria(i):
        count += 1
print(count)
