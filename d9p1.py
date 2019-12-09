import contextlib
import io
import operator
import sys
from os import path


def load_intcode():
    with open(f"{path.basename(__file__)[:2]}.txt") as f:  # Might as well make
        return [int(x) for x in f.read().split(",")]  # copy pasting easier


POINTER_INCREMENT = {
    1: 4,
    2: 4,
    3: 2,
    4: 2,
    5: 3,
    6: 3,
    7: 4,
    8: 4,
    9: 2,
    99: 0
}
NO_TARGET = [4, 5, 6, 9]


class Memory(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if key > len(self) - 1:
            self.extend([0] * (key - len(self) + 2))
        return super().__setitem__(key, value)

    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.stop > len(self) - 1:
                return [0] * (index.stop - index.start + 1)
        else:
            if index > len(self) - 1:
                return 0
        return super().__getitem__(index)


class Instruction:
    def __init__(self, computer):
        self.computer = computer
        self.mem = computer.mem
        code = str(self.mem[computer.pointer])
        self.code = code
        self.opcode = int(code[-2:])
        if self.opcode == 99:
            return
        self.increment = POINTER_INCREMENT[self.opcode]
        parameters = self.mem[computer.pointer + 1:computer.pointer +
                              self.increment]
        instructions = code[:-2]
        self.parameters = []
        parameter_modes = list(reversed([int(i) for i in instructions]))
        parameter_modes += [0] * (len(parameters) - len(parameter_modes))
        if self.opcode not in NO_TARGET:
            self.target = parameters[-1]
            mode = parameter_modes[-1]
            if mode == 2:
                self.target += self.computer.relative_base
            parameters = parameters[:-1]
            parameter_modes = parameter_modes[:-1]
        for parameter, mode in zip(parameters, parameter_modes):
            if mode == 1:
                self.parameters.append(parameter)
                continue
            elif mode == 2:
                self.parameters.append(
                    self.mem[self.computer.relative_base + parameter])
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
        if self.opcode == 9:
            self.increment_pointer()
            self.computer.relative_base += self.parameters[0]
            return


class Computer:
    def __init__(self, intcode):
        self.mem = Memory(intcode)
        self.pointer = 0
        self.relative_base = 0
        self.inputs = []

    def run(self, *, stop_on_stdout=False):
        if self.inputs:
            sys.stdin = io.StringIO("".join(f"{x}\n" for x in self.inputs))
        f = io.StringIO()
        output = []
        with contextlib.redirect_stdout(f):
            return_code = None
            while return_code != 0:
                instruction = Instruction(self)
                return_code = instruction.execute()
                if return_code == 1:
                    value = int(f.getvalue())
                    if stop_on_stdout:
                        return value
                    output.append(value)
                    f.truncate(0)
                    f.seek(0)
        for value in output:
            print(value)


computer = Computer(load_intcode())
computer.run()
