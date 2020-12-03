import math
from itertools import count

from util import ManyLineInput


def count_trees(input, right, down):
    width = len(input[0])
    coords_and_row = zip(count(0, right), input[::down])
    return sum(map(lambda cr: cr[1][cr[0] % width] == '#', coords_and_row))


def part1():
    with ManyLineInput('./input.txt') as data:
        tree_count = count_trees(data, 3, 1)
        print(f"part 1: {tree_count}")


def part2():
    with ManyLineInput('./input.txt') as data:
        angles = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        answer = math.prod(map(lambda angle: count_trees(data, angle[0], angle[1]), angles))
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
