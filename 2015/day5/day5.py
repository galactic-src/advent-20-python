import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


class SantaString:
    def __init__(self, s):
        self.s = s

    def is_nice(self):
        return self.got_three_vowels() and self.got_double_letter() and not self.contains_forbidden_pair()

    def got_three_vowels(self):
        return len([c for c in self.s if c in 'aeiou']) >= 3

    def got_double_letter(self):
        return any(map(lambda w: w[0] == w[1], windowed(self.s, 2)))

    def contains_forbidden_pair(self):
        return any(s in self.s for s in ['ab', 'cd', 'pq', 'xy'])


def part1():
    with ManyLineInput('./input.txt', SantaString) as data:
        print(f"part 1: {len([s for s in data if s.is_nice()])}")


class SantaString2:
    four_in_a_row = re.compile(r"(.)\1\1\1")
    three_in_a_row = re.compile(r"(.)\1\1")

    def __init__(self, s):
        self.s = s

    def is_nice(self):
        return self.got_matching_pairs() and self.got_split_pair()

    def got_matching_pairs(self):
        # cannot overlap - 4 in a row is a match, 3 in a row is not
        if SantaString2.four_in_a_row.match(self.s):
            return True

        without_triples = SantaString2.three_in_a_row.sub(lambda m: m.group(1) * 2, self.s)
        c = collections.Counter(windowed(without_triples, 2))
        return any(map(lambda v: v >= 2, c.values()))

    def got_split_pair(self):
        return any(map(lambda w: w[0] == w[2], windowed(self.s, 3)))


def part2():
    with ManyLineInput('./input.txt', SantaString2) as data:
        print(f"part 2: {len([s for s in data if s.is_nice()])}")


if __name__ == "__main__":
    part1()

    part2()  # 399 too high, not 63



