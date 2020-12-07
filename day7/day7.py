import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


class BagRule:
    def __init__(self, s):
        s = s.rstrip('.')
        self.container, remainder = s.split(' contain ')
        self.container = self.container[:-1]  # strip s
        self.targets = [t.split(' ', 1) for t in remainder.split(', ')] if remainder != 'no other bags' else []
        for target in self.targets:
            target[0] = int(target[0])
            if target[1].endswith('s'):
                target[1] = target[1][:-1]


def in_gold(rule, results, rules):
    if rule.container in results:
        return results[rule.container]

    if any(map(lambda t: rules[t[1]].container == 'shiny gold bag', rule.targets)):
        results[rule.container] = True
    elif any(map(lambda r: in_gold(rules[r[1]], results, rules), rule.targets)):
        results[rule.container] = True
    else:
        results[rule.container] = False

    return results[rule.container]


def contained_bags(bag, rules, counts):
    if bag.container not in counts:
        if len(bag.targets) == 0:
            counts[bag.container] = 0
        else:
            counts[bag.container] = sum([target[0] * (contained_bags(rules[target[1]], rules, counts) + 1) for target in bag.targets])
    return counts[bag.container]


def part1():
    with ManyLineInput('./input.txt', BagRule) as data:
        results = dict()
        rules = {rule.container: rule for rule in data}
        for rule in data:
            in_gold(rule, results, rules)
        print(f"part 1: {len([result for result in results.values() if result is True])}")


def part2():
    with ManyLineInput('./input.txt', BagRule) as data:
        rules = {rule.container: rule for rule in data}
        answer = contained_bags(rules['shiny gold bag'], rules, counts=dict())
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
