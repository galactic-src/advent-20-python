import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, DelimitedLinesBlockInput


def wrap(grid, wrap_with):
    new_width = len(grid[0]) + 2
    return [[wrap_with] * new_width] + [[wrap_with] + line + [wrap_with] for line in grid] + [[wrap_with] * new_width]


def initial_wrap(grid, wrap_with):
    for _ in range(3):
        grid = wrap(grid, wrap_with)
    return grid


def count_lit(grid):
    return sum(sum(c == '#' for c in line) for line in grid)


def apply_kernel(grid, pattern, step):
    new_grid = []
    for ixy in range(1, len(grid)-3):
        new_line = []
        for ixx in range(1, len(grid[0])-3):
            # print(f"({ixx}, {ixy})")
            binary = "".join('1' if grid[y][x] == '#' else '0' for y in range(ixy, ixy+3) for x in range(ixx, ixx+3))
            # print(binary)
            pattern_ix = int(binary, 2)
            # print(pattern_ix)
            new_line.append(pattern[pattern_ix])
        new_grid.append(new_line)

    wrap_with = '#' if step % 2 == 0 else '.'
    return initial_wrap(new_grid, wrap_with)


def print_grid(grid):
    for line in grid:
        print("".join(line))
    print("")


def part1():
    with DelimitedLinesBlockInput('./input.txt') as data:
        pattern = data[0][0]
        grid = initial_wrap([[c for c in s] for s in data[1]], '.')
        print_grid(grid)

        grid = apply_kernel(grid, pattern, 0)
        print_grid(grid)

        grid = apply_kernel(grid, pattern, 1)
        print_grid(grid)

        # 5747 high
        print(f"part 1: {count_lit(grid)}")


def part2():
    with DelimitedLinesBlockInput('./input.txt') as data:
        pattern = data[0][0]
        grid = initial_wrap([[c for c in s] for s in data[1]], '.')
        print_grid(grid)

        for step in range(50):
            print(f"STEP {step+1}")
            grid = apply_kernel(grid, pattern, step)
            print_grid(grid)

        print(f"part 2: {count_lit(grid)}")


if __name__ == "__main__":
    part1()
    part2()