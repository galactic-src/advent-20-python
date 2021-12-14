from collections import Counter, defaultdict

from util import DelimitedLinesBlockInput


def parse_rules_1(rules):
    return {parts[0]: parts[1] for parts in map(lambda l: l.split(" -> "), rules)}


def step(polymer, rules):
    next_polymer = ""
    for a, b in zip(polymer, polymer[1:] + '.'):
        next_polymer += a
        next_polymer += rules[a+b] if a+b in rules else ""
    return next_polymer


def part1():
    with DelimitedLinesBlockInput('./input.txt') as data:
        polymer = data[0][0]
        rules = parse_rules_1(data[1])

        for _ in range(10):
            polymer = step(polymer, rules)

        counter = Counter(polymer)

        sorted_counts = counter.most_common()
        answer = sorted_counts[0][1] - sorted_counts[-1][1]
        print(f"part 1: {answer}")


def part2():
    with DelimitedLinesBlockInput('./input.txt') as data:
        polymer = data[0][0]
        rules = dict()
        for line in data[1]:
            parts = line.split(" -> ")
            rules[parts[0]] = (parts[0][0] + parts[1], parts[1] + parts[0][1])

        pairs = defaultdict(int)
        for i in range(len(polymer)-1):
            pairs[polymer[i:i+2]] += 1

        last = polymer[-2:]

        for i in range(40):
            new_pairs = defaultdict(int)
            for pair, count in pairs.items():
                new_pair1, new_pair2 = rules[pair]
                new_pairs[new_pair1] += count
                new_pairs[new_pair2] += count
            pairs = new_pairs
            last = rules[last][1]

        counts = defaultdict(int)
        for pair, count in pairs.items():
            counts[pair[0]] += count
        counts[last[1]] += 1

        print(f"part 2: {max(counts.values()) - min(counts.values())}")


if __name__ == "__main__":
    part1()
    part2()
