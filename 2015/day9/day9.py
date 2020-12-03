import collections
from enum import Enum, auto
import re
from functools import reduce
from itertools import combinations, accumulate, permutations

from util import ManyLineInput, OneLineInput, windowed


class Distance:
    def __init__(self, s):
        locations, distance = s.split(' = ')
        self.distance = int(distance)
        self.locations = tuple(sorted(locations.split(' to ')))


def part1():
    with ManyLineInput('./input.txt', Distance) as data:
        distances = {d.locations: d.distance for d in data}
        locations = reduce(lambda s, d: set(d.locations).union(s), data, set())
        answer = min(map(lambda selection: sum(map(lambda w: distances[tuple(sorted(w))], windowed(selection, 2))), permutations(locations, len(locations))))
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', Distance) as data:
        distances = {d.locations: d.distance for d in data}
        locations = reduce(lambda s, d: set(d.locations).union(s), data, set())
        answer = max(map(lambda selection: sum(map(lambda w: distances[tuple(sorted(w))], windowed(selection, 2))),
                         permutations(locations, len(locations))))
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

