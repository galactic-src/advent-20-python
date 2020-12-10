import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


MFCSAM = {'children': 3,
          'cats': 7,
          'samoyeds': 2,
          'pomeranians': 3,
          'akitas': 0,
          'vizslas': 0,
          'goldfish': 5,
          'trees': 3,
          'cars': 2,
          'perfumes': 1}

class Aunt:
    def __init__(self, s):
        name, prop_s = s.split(": ")
        self.id = int(name[4:])
        print(prop_s)
        print(list(prop_s.split(', ')))
        self.props = {el.split[': '][0]: int(el.split[': '][1]) for el in prop_s.split(', ')}


def props_match(aunt):
    for k, v in aunt.items():
        if MFCSAM[k] != v:
            return False
    else:
        return True


def part1():
    with ManyLineInput('./input.txt', Aunt) as data:
        answer = next(filter(props_match, data))
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt') as data:
        answer = ''
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    # part2()

