import collections
from enum import Enum, auto
import re
import math
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, partitions, p, plist


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


def product(ingredient_and_quantity):
    properties = set(ingredient_and_quantity[0][0].keys())
    sums = [max(sum(iq[0][property] * iq[1] for iq in ingredient_and_quantity), 0) for property in properties if property != 'calories']
    return math.prod(sums)


def product2(ingredient_and_quantity):
    properties = set(ingredient_and_quantity[0][0].keys())
    if sum(iq[0]['calories'] * iq[1] for iq in ingredient_and_quantity) != 500:
        return 0
    sums = [max(sum(iq[0][property] * iq[1] for iq in ingredient_and_quantity), 0) for property in properties if property != 'calories']
    return math.prod(sums)


def part1():
    with ManyLineInput('./input.txt', Ingredient) as data:
        answer = max([product(list(zip(data, partition))) for partition in partitions(len(data), 100)])
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', Ingredient) as data:
        answer = max([product2(list(zip(data, partition))) for partition in partitions(len(data), 100)])
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

