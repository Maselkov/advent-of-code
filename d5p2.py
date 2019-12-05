import operator

SOUGHT = 19690720
with open("d5.txt") as f:
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
            exit()
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
        if self.opcode in (1, 2):
            func = {1: operator.add, 2: operator.mul}.get(self.opcode)
            value = func(*self.parameters)
            self.increment_pointer()
            return self.write(value)
        if self.opcode == 3:
            value = int(input("Input the value:\n"))
            self.increment_pointer()
            return self.write(value)
        if self.opcode == 4:
            self.increment_pointer()
            return print(self.parameters[0])
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
            if func(*self.parameters[:2]):
                return self.write(1)
            return self.write(0)


class Computer:
    def __init__(self, memory):
        self.mem = memory
        self.pointer = 0

    def run(self):
        while True:
            instruction = Instruction(self)
            instruction.execute()


comp = Computer(intcode)
comp.run()
