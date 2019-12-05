import operator

with open("d5.txt") as f:
    intcode = [int(x) for x in f.read().split(",")]

POINTER_INCREMENT = {1: 4, 2: 4, 3: 2, 4: 2, 99: 0}


class Instruction:
    def __init__(self, computer):
        self.mem = computer.mem
        code = str(self.mem[computer.pointer])
        self.opcode = int(code[-2:])
        if self.opcode == 99:
            exit()
        self.increment = POINTER_INCREMENT[self.opcode]
        parameters = self.mem[computer.pointer + 1:computer.pointer +
                              self.increment]
        instructions = code[:-2]
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

    def execute(self):
        if self.opcode in (1, 2):
            func = {1: operator.add, 2: operator.mul}.get(self.opcode)
            value = func(*self.parameters)
            return self.write(value)
        if self.opcode == 3:
            value = int(input("Input the value:\n"))
            return self.write(value)
        if self.opcode == 4:
            return print(self.mem[self.target])


class Computer:
    def __init__(self, memory):
        self.mem = memory
        self.pointer = 0

    def run(self):
        while True:
            instruction = Instruction(self)
            instruction.execute()
            self.pointer += instruction.increment


comp = Computer(intcode)
comp.run()
