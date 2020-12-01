import collections
from enum import Enum, auto
import math
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


def solve(inputs, count):
    for selection in combinations(inputs, count):
        if sum(selection) == 2020:
            return math.prod(selection)


def part1():
    with ManyLineInput('./input.txt', int) as data:
        print(f"part 1: {solve(data, 2)}")


def part2():
    with ManyLineInput('./input.txt', int) as data:
        print(f"part 2: {solve(data, 3)}")


if __name__ == "__main__":
    part1()
    part2()

