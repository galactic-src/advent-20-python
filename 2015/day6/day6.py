import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

import numpy as np

from util import ManyLineInput, OneLineInput, windowed


class InstructionType(Enum):
    ON = auto(),
    OFF = auto(),
    TOGGLE = auto()


class LightInstruction:
    coord_re = re.compile(r'(\d+),(\d+) through (\d+),(\d+)')

    def __init__(self, s: str):
        self.instruction_type, remainder = self.parse_type(s)
        m = LightInstruction.coord_re.fullmatch(remainder)
        self.x1 = int(m.group(1))
        self.y1 = int(m.group(2))
        self.x2 = int(m.group(3))
        self.y2 = int(m.group(4))

    @staticmethod
    def parse_type(s: str):
        if s.startswith('turn on '):
            return InstructionType.ON, s[len('turn on '):]
        elif s.startswith('turn off '):
            return InstructionType.OFF, s[len('turn off '):]
        elif s.startswith('toggle '):
            return InstructionType.TOGGLE, s[len('toggle '):]

    def __repr__(self):
        return f"{self.instruction_type.name} ({self.x1},{self.y1}) -> ({self.x2},{self.y2})"


class Grid1:
    def __init__(self):
        self.data = np.full((1000, 1000), False)

    def apply(self, instruction):
        if instruction.instruction_type is InstructionType.ON:
            self.data[instruction.y1:instruction.y2+1, instruction.x1:instruction.x2+1] = True
        elif instruction.instruction_type is InstructionType.OFF:
            self.data[instruction.y1:instruction.y2+1, instruction.x1:instruction.x2+1] = False
        elif instruction.instruction_type is InstructionType.TOGGLE:
            self.data[instruction.y1:instruction.y2 + 1, instruction.x1:instruction.x2 + 1] = \
                np.invert(self.data[instruction.y1:instruction.y2 + 1, instruction.x1:instruction.x2 + 1])
        else:
            raise Exception("apply went wrong")

    def count_on(self):
        return np.asarray(self.data).sum()


def part1():
    with ManyLineInput('./input.txt', LightInstruction) as data:
        grid = Grid1()
        for instruction in data:
            grid.apply(instruction)
        print(f"part 1: {grid.count_on()}")


class Grid2:
    def __init__(self):
        self.data = np.zeros((1000, 1000), dtype=np.int32)

    def apply(self, instruction):
        if instruction.instruction_type is InstructionType.ON:
            self.data[instruction.y1:instruction.y2+1, instruction.x1:instruction.x2+1] += 1
        elif instruction.instruction_type is InstructionType.OFF:
            dx = instruction.x2 - instruction.x1 + 1
            dy = instruction.y2 - instruction.y1 + 1
            self.data[instruction.y1:instruction.y2+1, instruction.x1:instruction.x2+1] = \
                np.maximum(self.data[instruction.y1:instruction.y2+1, instruction.x1:instruction.x2+1] - 1,
                           np.zeros((dy, dx), dtype=np.int32))
        elif instruction.instruction_type is InstructionType.TOGGLE:
            self.data[instruction.y1:instruction.y2 + 1, instruction.x1:instruction.x2 + 1] += 2
        else:
            raise Exception("apply went wrong")

    def count_on(self):
        return np.asarray(self.data).sum()


def part2():
    with ManyLineInput('./input.txt', LightInstruction) as data:
        grid = Grid2()
        for instruction in data:
            grid.apply(instruction)
        print(f"part 2: {grid.count_on()}")


if __name__ == "__main__":
    part1()
    part2()  # 13396307 is too low, 19654607 is too high
