import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate, permutations

from util import ManyLineInput, OneLineInput, windowed


class HappyDelta:
    def __init__(self, s):
        self.s = s
        self.subject, remaining = s.split(' would ')
        delta, remaining = remaining.split(' happiness units by sitting next to ')
        self.target = remaining.rstrip('.')
        if delta.startswith('gain '):
            self.delta = int(delta[len('gain '):])
        elif delta.startswith('lose '):
            self.delta = -(int(delta[len('lose '):]))
        else:
            raise Exception(f"delta {delta}")

    def __repr__(self):
        return f"{self.s} => {self.subject}-{self.target} = {self.delta}"


def max_happiness(data):
    people = {h.subject for h in data}
    happyLookup = {(hd.subject, hd.target): hd.delta for hd in data}
    cycles = list(map(lambda p: list(p) + [p[0]], permutations(people)))
    happySums = list(map(lambda c: sum([happyLookup[(w[0], w[1])] + happyLookup[(w[1], w[0])] for w in windowed(c, 2)]), cycles))
    return max(happySums)


def part1():
    with ManyLineInput('./input.txt', HappyDelta) as data:
        print(f"part 1: {max_happiness(data)}")


def part2():
    with ManyLineInput('./input.txt', HappyDelta) as data:
        people = {h.subject for h in data}
        data.extend([HappyDelta(f'Me would gain 0 happiness units by sitting next to {person}.') for person in people])
        data.extend([HappyDelta(f'{person} would gain 0 happiness units by sitting next to Me.') for person in people])
        print(f"part 2: {max_happiness(data)}")


if __name__ == "__main__":
    part1()
    part2()
