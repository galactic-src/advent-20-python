import collections
from enum import Enum, auto
import re
import math
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, partitions, p


class Ingredient(dict):
    def __init__(self, s):
        super().__init__()
        self.name, remainder = s.split(": capacity ")
        capacity, remainder = remainder.split(", durability ")
        self['capacity'] = int(capacity)
        durability, remainder = remainder.split(", flavor ")
        self['durability'] = int(durability)
        flavor, remainder = remainder.split(", texture ")
        self['flavor'] = int(flavor)
        texture, calories = remainder.split(", calories")
        self['texture'] = int(texture)
        self['calories'] = int(calories)


def product(ingredients, quantities):
    return math.prod([sum([ingredient[property] for ingredient in ingredients]) * quantities[property] for property in ingredients[0].keys()])


def part1():
    with ManyLineInput('./input.txt', Ingredient) as data:
        names = list(data[0].keys())
        answer = max([product(data, {z[0]: z[1] for z in zip(names, partition)}) for partition in partitions(len(names), 100)])
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt') as data:
        answer = ''
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()  # 384000000 too high
    # part2()

