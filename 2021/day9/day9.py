from math import prod
from util import ManyLineInput


def make_grid():
    with ManyLineInput('./input.txt') as data:
        width = len(data[0])
        grid = [(width + 2) * [10]] + [[10] + [int(c) for c in line] + [10] for line in data] + [(width + 2) * [10]]
        return grid


def low_points(grid):
    total = 0
    result = []
    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[0])-1):
            val = grid[i][j]
            if all(val < grid[x][y] for (x, y) in [(i-1, j), (i, j-1), (i+1, j), (i, j+1)]):
                result.append((i, j))
                total += val+1
    return result


def part1():
    grid = make_grid()
    lps = low_points(grid)

    total = sum(grid[x][y]+1 for (x, y) in lps)

    print(f"part 1: {total}")


def basin_size(low_point, grid):
    points = set()
    points.add(low_point)
    to_explore = {low_point}
    while len(to_explore):
        lpx, lpy = to_explore.pop()
        val = grid[lpx][lpy]
        for x, y in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
            next_val = grid[lpx+x][lpy+y]
            if val < next_val < 9:
                if (lpx+x, lpy+y) not in points:
                    to_explore.add((lpx+x, lpy+y))
                    points.add((lpx+x, lpy+y))
    return len(points)


def part2():
    grid = make_grid()
    lps = low_points(grid)

    basin_sizes = [basin_size(lp, grid) for lp in lps]
    basin_sizes = sorted(basin_sizes)

    answer = prod(basin_sizes[-3:])
    print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
