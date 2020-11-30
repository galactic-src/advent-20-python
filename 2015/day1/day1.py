from itertools import accumulate

from util import OneLineInput


def part1():
    with OneLineInput('./input.txt') as data:
        print(f"part 1: {sum(map(convert_bracket, data))}")


def convert_bracket(b):
    if b == '(':
        return 1
    elif b == ')':
        return -1
    else:
        raise ValueError(f"'{b}' is not a bracket")


def part2():
    with OneLineInput('./input.txt') as data:
        totals = [total for total in accumulate(map(convert_bracket, data))]
        print(f"part 2: {totals.index(-1) + 1}")


if __name__ == "__main__":
    part1()
    part2()
