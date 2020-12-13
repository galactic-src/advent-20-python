import collections
from enum import Enum, auto
import re
from functools import reduce

from util import ManyLineInput


class Direction(Enum):
    North = auto(),
    South = auto(),
    East = auto(),
    West = auto()


class Instruction:
    RX = re.compile(r'([A-Z])(\d+)')

    def __init__(self, s):
        self.letter, number = Instruction.RX.fullmatch(s).groups()
        self.number = int(number)


def left(d):
    if d == Direction.North:
        return Direction.West
    elif d == Direction.West:
        return Direction.South
    elif d == Direction.South:
        return Direction.East
    elif d == Direction.East:
        return Direction.North
    else:
        raise Exception(f"direction {d}")


def right(d):
    if d == Direction.North:
        return Direction.East
    elif d == Direction.East:
        return Direction.South
    elif d == Direction.South:
        return Direction.West
    elif d == Direction.West:
        return Direction.North
    else:
        raise Exception(f"direction {d}")


def manhattan(ew, ns):
    return abs(ew) + abs(ns)


def apply_instruction(t, i: Instruction):
    x, y, direction = t
    if i.letter == 'E' or (i.letter == 'F' and direction == Direction.East):
        return x + i.number, y, direction
    elif i.letter == 'W' or (i.letter == 'F' and direction == Direction.West):
        return x - i.number, y, direction
    elif i.letter == 'N' or (i.letter == 'F' and direction == Direction.North):
        return x, y + i.number, direction
    elif i.letter == 'S' or (i.letter == 'F' and direction == Direction.South):
        return x, y - i.number, direction
    elif i.letter == 'L':
        for _ in range(int(i.number/90)):
            direction = left(direction)
        return x, y, direction
    elif i.letter == 'R':
        for _ in range(int(i.number/90)):
            direction = right(direction)
        return x, y, direction
    else:
        raise Exception(f"instruction {i.letter} {i.number}")


def left2(dx, dy):
    return -dy, dx


def right2(dx, dy):
    return dy, -dx


def apply_instruction_2(t, i: Instruction):
    x, y, dx, dy = t
    if i.letter == 'E':
        return x, y, dx + i.number, dy
    elif i.letter == 'W':
        return x, y, dx - i.number, dy
    elif i.letter == 'N':
        return x, y, dx, dy + i.number
    elif i.letter == 'S':
        return x, y, dx, dy - i.number
    elif i.letter == 'L':
        for _ in range(int(i.number/90)):
            dx, dy = left2(dx, dy)
        return x, y, dx, dy
    elif i.letter == 'R':
        for _ in range(int(i.number/90)):
            dx, dy = right2(dx, dy)
        return x, y, dx, dy
    elif i.letter == 'F':
        return x+dx*i.number, y+dy*i.number, dx, dy
    else:
        raise Exception(f"instruction {i.letter} {i.number}")


def part1():
    with ManyLineInput('./input.txt', Instruction) as data:
        x, y, d = reduce(apply_instruction, data, (0, 0, Direction.East))
        answer = manhattan(x, y)
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', Instruction) as data:
        x, y, dx, dy = reduce(apply_instruction_2, data, (0, 0, 10, 1))
        answer = manhattan(x, y)
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

