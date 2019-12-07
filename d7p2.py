import contextlib
import io
import itertools
import operator
import sys

with open("d7.txt") as f:
    intcode = [int(x) for x in f.read().split(",")]

POINTER_INCREMENT = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 99: 0}
NO_TARGET = [4, 5, 6]


class Instruction:
    def __init__(self, computer):
        self.computer = computer
        self.mem = computer.mem
        code = str(self.mem[computer.pointer])
        self.opcode = int(code[-2:])
        if self.opcode == 99:
            return
        self.increment = POINTER_INCREMENT[self.opcode]
        parameters = self.mem[computer.pointer + 1:computer.pointer +
                              self.increment]
        instructions = code[:-2]
        if self.opcode not in NO_TARGET:
            self.target = parameters[-1]
            parameters = parameters[:-1]
        self.parameters = []
        parameter_modes = list(reversed([int(i) for i in instructions]))
        parameter_modes += [0] * (len(parameters) - len(parameter_modes))
        for parameter, mode in zip(parameters, parameter_modes):
            if mode == 1:
                self.parameters.append(parameter)
                continue
            self.parameters.append(self.mem[parameter])

    def write(self, result):
        self.mem[self.target] = result

    def increment_pointer(self):
        self.computer.pointer += self.increment

    def execute(self):
        if self.opcode == 99:
            return 0
        if self.opcode in (1, 2):
            func = {1: operator.add, 2: operator.mul}.get(self.opcode)
            value = func(*self.parameters)
            self.increment_pointer()
            return self.write(value)
        if self.opcode == 3:
            value = int(input())
            self.increment_pointer()
            return self.write(value)
        if self.opcode == 4:
            self.increment_pointer()
            print(self.parameters[0])
            return 1
        if self.opcode == 5:
            if self.parameters[0]:
                self.computer.pointer = self.parameters[1]
                return
            return self.increment_pointer()
        if self.opcode == 6:
            if not self.parameters[0]:
                self.computer.pointer = self.parameters[1]
                return
            return self.increment_pointer()
        if self.opcode in (7, 8):
            self.increment_pointer()
            func = {7: operator.lt, 8: operator.eq}.get(self.opcode)
            if func(*self.parameters):
                return self.write(1)
            return self.write(0)


class Computer:
    def __init__(self, memory):
        self.mem = memory
        self.pointer = 0
        self.inputs = []

    def run(self, *, stop_on_stdout=False):
        sys.stdin = io.StringIO("".join(f"{x}\n" for x in self.inputs))
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            return_code = None
            while return_code != 0:
                instruction = Instruction(self)
                return_code = instruction.execute()
                if stop_on_stdout and return_code == 1:
                    return int(f.getvalue())
            return None


HIGHEST_VALUE = 0

for combination in itertools.permutations(range(5, 10)):
    amp_computers = [Computer(intcode) for _ in range(5)]
    thrust_value = 0
    for phase, computer in zip(combination, amp_computers):
        computer.inputs = [phase, thrust_value]
        thrust_value = computer.run(stop_on_stdout=True)
    while True:
        for computer in amp_computers:
            computer.inputs = [thrust_value]
            result = computer.run(stop_on_stdout=True)
            if result is None:
                break
            thrust_value = result
        else:
            continue
        break
    if thrust_value > HIGHEST_VALUE:
        HIGHEST_VALUE = thrust_value
print(HIGHEST_VALUE)
