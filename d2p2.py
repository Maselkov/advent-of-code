import copy
import operator

OPCODES = {1: operator.add, 2: operator.mul, 99: None}
SOUGHT = 19690720
with open("d2.txt") as f:
    intcode = [int(x) for x in f.read().split(",")]


def execute(mem, verb, noun):
    mem[1] = verb
    mem[2] = noun
    current_pos = 0
    while True:
        opcode = mem[current_pos]
        if opcode == 99:
            break
        # This is basically a switch statement, getting the correct operator
        op = OPCODES.get(opcode)
        # Using the operator on the two values pointed at by positions of two
        # following values after opcode
        value = op(*[mem[mem[current_pos + i]] for i in range(1, 3)])
        position_to_replace = mem[current_pos + 3]
        mem[position_to_replace] = value
        current_pos += 4
    return mem[0]


for verb in range(100):
    for noun in range(100):
        if execute(copy.copy(intcode), verb, noun) == SOUGHT:
            print(100 * verb + noun)
