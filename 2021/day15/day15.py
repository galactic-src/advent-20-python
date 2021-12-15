import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, DelimitedLinesBlockInput


class Explorer:
    def __init__(self, risks, height, width):
        self.risks = risks
        self.height = height
        self.width = width
        self.could_explore = dict()
        self.reached = dict()

    def find_next(self):
        best_risk = None
        best_loc = None
        for loc, risk in self.could_explore.items():
            if best_risk is None or best_risk > risk:
                best_risk = risk
                best_loc = loc
        return best_loc, best_risk

    def explore(self, dest_x, dest_y):
        self.could_explore[(0,0)] = 0

        while self.could_explore:
            loc, risk = self.find_next()

            if loc == (dest_x, dest_y):
                return risk
            else:
                self.reached[loc] = risk
                del self.could_explore[loc]
                for x, y in [(loc[0]+dx, loc[1]+dy) for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]]:
                    if 0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.reached:
                        possible = (x, y)
                        possible_risk = risk + self.risks[possible]
                        if (x, y) in self.could_explore:
                            self.could_explore[possible] = min(possible_risk, self.could_explore[possible])
                        else:
                            self.could_explore[possible] = possible_risk


def part1():
    with ManyLineInput('./input.txt') as data:
        risks = {(x, y): int(data[y][x]) for x in range(len(data[0])) for y in range(len(data))}
        height = len(data)
        width = len(data[0])
        explorer = Explorer(risks, height, width)

    best_risk = explorer.explore(explorer.width-1, explorer.height-1)

    print(f"part 1: {best_risk}")


def part2():
    extended = []
    with ManyLineInput('./input.txt') as data:
        for j in range(5):
            for y in range(len(data)):
                line = []
                for i in range(5):
                    for x in range(len(data[0])):
                        val = int(data[y][x]) + i + j
                        while val > 9:
                            val -= 9
                        line.append(val)
                extended.append(line)

    risks = {(x, y): int(extended[y][x]) for x in range(len(extended[0])) for y in range(len(extended))}
    explorer = Explorer(risks, len(extended), len(extended[0]))

    best_risk = explorer.explore(explorer.width-1, explorer.height-1)

    print(f"part 2: {best_risk}")


if __name__ == "__main__":
    part1()
    part2()