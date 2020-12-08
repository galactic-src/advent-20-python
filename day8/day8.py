from util import ManyLineInput


class Inst:
    def __init__(self, s):
        self.name, remainder = s.split(" ")
        self.arg = int(remainder)


class Machine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.ip = 0
        self.acc = 0
        self.visited = set()
        self.normal = None

    def execute(self, program):
        while True:
            if self.ip == len(program):
                self.normal = True
                break

            if self.ip > len(program) or self.ip in self.visited:
                self.normal = False
                break

            self.visited.add(self.ip)

            ins = program[self.ip]
            if ins.name == 'nop':
                self.ip += 1
            elif ins.name == 'acc':
                self.acc += ins.arg
                self.ip += 1
            elif ins.name == 'jmp':
                self.ip += ins.arg
            else:
                print(f"instruction@{self.ip}: {ins.name}({ins.arg})")


def part1():
    with ManyLineInput('./input.txt', Inst) as program:
        machine = Machine()
        machine.execute(program)
        answer = machine.acc
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', Inst) as program:
        answer = None
        for ix, inst in enumerate(program):
            if inst.name in ['jmp', 'nop']:
                machine = Machine()
                prog = [Inst(f"{i.name} {i.arg}") for i in program]
                if inst.name == 'jmp':
                    prog[ix].name = 'nop'
                elif inst.name == 'nop':
                    prog[ix].name = 'jmp'
                machine.execute(prog)
                if machine.normal:
                    answer = machine.acc
                    break

    answer = answer or "nothing terminated normally"
    print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
