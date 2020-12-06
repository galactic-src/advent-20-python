import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, DelimitedLinesBlockInput


def part1():
    with DelimitedLinesBlockInput('./input.txt') as data:
        answer = sum(map(lambda block: len(set(c for c in "".join(block))), data))
        print(f"part 1: {answer}")


def part2():
    with DelimitedLinesBlockInput('./input.txt') as data:
        answer = sum(map(lambda block: len(set.intersection(*[{c for c in line} for line in block])), data))
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

