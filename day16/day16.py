from math import prod

from util import DelimitedLinesBlockInput


class Rule:
    def __init__(self, s):
        self.name, ranges = s.split(': ')
        r1, r2 = ranges.split(' or ')
        self.r1lo, self.r1hi = map(int, r1.split('-'))
        self.r2lo, self.r2hi = map(int, r2.split('-'))

    def valid(self, val):
        return self.r1lo <= val <= self.r1hi or self.r2lo <= val <= self.r2hi


def part1():
    with DelimitedLinesBlockInput('./input.txt') as data:
        rules = [Rule(s) for s in data[0]]
        rate = sum(v for t in data[2][1:] for v in map(int, t.split(',')) if not any(rule.valid(v) for rule in rules))
        print(f"part 1: {rate}")


def part2():
    with DelimitedLinesBlockInput('./input.txt') as data:
        rules = [Rule(s) for s in data[0]]
        fields = set(r.name for r in rules)
        target_fields = set(r.name for r in rules if r.name.startswith('departure'))

        other_tickets = [[int(v) for v in ticket.split(',')] for ticket in data[2][1:]]
        valid_tickets = [t for t in other_tickets if all(any(rule.valid(v) for rule in rules) for v in t)]
        zipped_tickets = []
        for z in zip(*valid_tickets):
            zipped_tickets.append(list(z))
        possibles = [{rule.name for rule in rules if all(rule.valid(v) for v in z)} for z in zipped_tickets]

        remaining = list(fields)
        confirmed = dict()
        while remaining:
            for ix, poss in enumerate(possibles):
                if len(poss) == 1:
                    name = next(iter(poss))
                    break
            else:
                "didn't find any"
                break
            confirmed[name] = ix
            remaining.remove(name)
            for poss in possibles:
                poss.discard(name)

        mine = [int(v) for v in data[1][1].split(',')]
        print(f"part 2: {prod(mine[confirmed[t]] for t in target_fields)}")


if __name__ == "__main__":
    part1()
    part2()

