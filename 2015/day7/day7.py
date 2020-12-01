import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


class GateType(Enum):
    INPUT = auto(),
    NOT = auto(),
    AND = auto(),
    LSHIFT = auto(),
    RSHIFT = auto(),
    OR = auto()


class GateInput:
    def __init__(self, tok):
        self.tok = tok

    def available(self, resolved):
        return self.tok.isnumeric() or self.tok in resolved

    def resolve(self, resolved):
        if self.tok.isnumeric():
            return int(self.tok)
        else:
            return resolved[self.tok]


class Gate:
    def __init__(self, s):
        self.inputs = []
        left, self.output = s.split(' -> ')
        input_toks = left.split(' ')
        if len(input_toks) == 1:
            self.inputs.append(GateInput(input_toks[0]))
            self.gate_type = GateType.INPUT
        elif len(input_toks) == 2:
            type_tok, input1 = input_toks
            self.gate_type = GateType[type_tok]
            self.inputs.append(GateInput(input1))
        elif len(input_toks) == 3:
            input1, type_tok, input2 = input_toks
            self.inputs.append(GateInput(input1))
            self.gate_type = GateType[type_tok]
            self.inputs.append(GateInput(input2))
        else:
            raise Exception(f"didn't expect {len(input_toks)} args")

    def output_value(self, resolved):
        if self.gate_type is GateType.INPUT:
            print(f"INPUT {self.inputs[0].resolve(resolved)}")
            out = self.inputs[0].resolve(resolved)
        elif self.gate_type is GateType.NOT:
            print(f"NOT ~{self.inputs[0].resolve(resolved)}")
            out = ~self.inputs[0].resolve(resolved)
        elif self.gate_type is GateType.AND:
            print(f"AND {self.inputs[0].resolve(resolved)} & {self.inputs[1].resolve(resolved)}")
            out = self.inputs[0].resolve(resolved) & self.inputs[1].resolve(resolved)
        elif self.gate_type is GateType.OR:
            print(f"OR {self.inputs[0].resolve(resolved)} | {self.inputs[1].resolve(resolved)}")
            out = self.inputs[0].resolve(resolved) | self.inputs[1].resolve(resolved)
        elif self.gate_type is GateType.LSHIFT:
            print(f"LSHIFT {self.inputs[1].resolve(resolved)} << {self.inputs[1].resolve(resolved)}")
            out = self.inputs[0].resolve(resolved) << self.inputs[1].resolve(resolved)
        elif self.gate_type is GateType.RSHIFT:
            print(f"RSHIFT {self.inputs[0].resolve(resolved)} >> {self.inputs[1].resolve(resolved)}")
            out = self.inputs[0].resolve(resolved) >> self.inputs[1].resolve(resolved)
        else:
            raise Exception(f'gate_type {self.gate_type}')

        if out > 65535:
            out %= 65535
        elif out < 0:
            out += 65535 + 1
        print(out)
        return out

    @staticmethod
    def parse_input(inpt):
        return int(inpt) if inpt.isnumeric() else inpt


def process_gates(gates):
    resolved = dict()
    inputs = collections.defaultdict(list)

    for g in gates:
        for i in g.inputs:
            if not i.tok.isnumeric():
                inputs[i.tok].append(g)
    print(inputs)

    newly_resolved = [g for g in gates if all([i.available(resolved) for i in g.inputs])]
    while len(newly_resolved):
        resolved_gate = newly_resolved.pop()
        resolved[resolved_gate.output] = resolved_gate.output_value(resolved)
        for g in inputs[resolved_gate.output]:
            if all([i.available(resolved) for i in g.inputs]) and g.output not in resolved:
                newly_resolved.append(g)
    print(resolved)
    if 'a' in resolved:
        return resolved['a']



def part1():
    with ManyLineInput('./input.txt', Gate) as data:
        print(f"part 1: {process_gates(data)}")


def part2():
    with ManyLineInput('./input.txt') as data:
        round1 = process_gates(data)
        data.remove()
        answer = ''
        print(f"part 2: {answer}")

if __name__ == "__main__":
    part1()
    # part2()

