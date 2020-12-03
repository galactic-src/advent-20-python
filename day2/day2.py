from collections import Counter

from util import ManyLineInput


class PasswordPolicy:
    def __init__(self, s):
        config, self.password = s.split(': ')
        letter_counts, self.letter = config.split(' ')
        lo, hi = letter_counts.split('-')
        self.lo = int(lo)
        self.hi = int(hi)


def is_in_range(val, lo, hi):
    return lo <= val <= hi


def count_letters_at_positions(p):
    return Counter(p.password[p.lo-1:p.hi])[p.letter]


def xor(a, b):
    return (a or b) and not (a and b)


def got_letter_at(p, ix):
    return len(p.password) >= ix and p.password[ix-1] == p.letter


def condition2(p):
    return xor(got_letter_at(p, p.lo), got_letter_at(p, p.hi))


def part1():
    with ManyLineInput('./input.txt', PasswordPolicy) as data:
        answer = len(list(filter(lambda p: is_in_range(Counter(p.password)[p.letter], p.lo, p.hi), data)))
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', PasswordPolicy) as data:
        answer = len(list(filter(lambda p: condition2(p), data)))
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

