import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


class ClassyClass:
    def __init__(self, s):
        pass
        #s = s.rstrip('.')
        #self.container, remainder = s.split(' contain ')
        #self.container = self.container[:-1]  # strip s
        #self.targets = [t.split(' ', 1) for t in remainder.split(', ')] if remainder != 'no other bags' else []
        #for target in self.targets:
        #    target[0] = int(target[0])
        #    if target[1].endswith('s'):
        #        target[1] = target[1][:-1]


def part1():
    with ManyLineInput('./input.txt') as data:
    #  with OneLineInput('./input.txt') as data:
        answer = ''
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt') as data:
    # with OneLineInput('./input.txt') as data:
        answer = ''
        print(f"part 2: {answer}")


if __name__ == "__main__":
    pass
    # part1()
    # part2()

