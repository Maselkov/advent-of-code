import operator

OPCODES = {1: operator.add, 2: operator.mul, 99: None}

with open("d2.txt") as f:
    intcode = [int(x) for x in f.read().split(",")]

current_pos = 0
while True:
    opcode = intcode[current_pos]
    if opcode == 99:
        break
    # This is basically a switch statement, getting the correct operator
    op = OPCODES.get(opcode)
    # Using the operator on the two values pointed at by positions of two
    # following values after opcode
    value = op(*[intcode[intcode[current_pos + i]] for i in range(1, 3)])
    position_to_replace = intcode[current_pos + 3]
    intcode[position_to_replace] = value
    current_pos += 4
print(intcode[0])
