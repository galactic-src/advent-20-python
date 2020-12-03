import collections
from enum import Enum, auto
import json
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


def is_numeric(j):
    return type(j) in [int, float]


def is_complex(j):
    return type(j) in [dict, list]


def sum_numerics(j, skip_red):
    if type(j) == dict:
        if "red" in j.values() and skip_red:
            return 0
        else:
            return sum(map(lambda j1: sum_numerics(j1, skip_red) if is_complex(j1) else j1 if is_numeric(j1) else 0, j.values()))
    elif type(j) == list:
        return sum(map(lambda j1: sum_numerics(j1, skip_red) if is_complex(j1) else j1 if is_numeric(j1) else 0, j))
    elif is_numeric(j):
        return j


def part1():
    with OneLineInput('./input.txt') as data:
        j = json.loads(data)
        answer = sum_numerics(j, False)
        print(f"part 1: {answer}")


def part2():
    with OneLineInput('./input.txt') as data:
        j = json.loads(data)
        answer = sum_numerics(j, True)
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

