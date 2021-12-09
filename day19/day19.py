import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, DelimitedLinesBlockInput

ALT = 'alternative'
SEQ = 'sequence'
LETTER = 'letter'
DEL = 'delegate'
REP = 'repeat'


class Rule:
    def __init__(self, s):
        if ": " in s:
            self.id, s = s.split(": ")
        else:
            self.id = None

        if '|' in s:
            self.type = ALT
            self.opts = [Rule(p) for p in s.split(' | ')]
        elif ' ' in s:
            sequence_rules = s.split(' ')
            if self.id and sequence_rules[-1] == self.id:
                self.type = REP
                sequence_rules = sequence_rules[:-1]
                print("repeat " + " ".join(sequence_rules))
            else:
                self.type = SEQ

            self.reqs = [Rule(p) for p in sequence_rules]
        elif '"' in s:
            self.type = LETTER
            self.letter = s.strip('"')
        elif s.isnumeric():
            self.type = DEL
            self.rule = s
        else:
            raise Exception("Rule()")

    def match(self, s, ix, rules, d='?'):
        print(f"rule {d}: checking ix {ix} {s[:ix]} {s[ix:]}")
        if ix == len(s):
            print('reached the end')
            return None
        
        if self.type == LETTER:
            matches = s[ix] == self.letter
            print(f'matching letter {self.letter} at ix {ix}: {matches}')
            return ix+1 if matches else None
        elif self.type == SEQ:
            for pix, part in enumerate(self.reqs):
                print(f"seq{pix}")
                test_ix = ix
                ix = part.match(s, ix, rules, d=f"{d}_{pix}")
                if ix is None:
                    print(f"didn't match {d.split(' ')[-1]} seq part {pix} at ix {test_ix}")
                    return None
            print(f"matched seq {d}")
            return ix
        elif self.type == ALT:
            matches = []
            for oix, opt in enumerate(self.opts):
                print(f"alt{oix}")
                matches = opt.match(s, ix, rules, d=f"{d}_{oix}")
                if matches > -1:
                    print(f"matched opt {oix}")
                    return matches
            else:
                print(f"didn't match any alternative at ix {ix}")
                return -1
        elif self.type == DEL:
            print(f'delegating to {self.rule}')
            return rules[self.rule].match(s, ix, rules, d=f"{d} > {self.rule}")
        else:
            raise Exception("match")


def rulebook(input):
    return {d.split(": ")[0]: Rule(d.split(": ")[1]) for d in input[0]}


def part1():
    with DelimitedLinesBlockInput('./ex2.txt') as data:
        rules = {d.split(": ")[0]: Rule(d) for d in data[0]}
        answer = len([1 for d in data[1] if rules['0'].match(d, 0, rules) == len(d)])
        print(f"part 1: {answer}")


def part2():
    with DelimitedLinesBlockInput('./ex2.txt') as data:
        rules = {d.split(": ")[0]: Rule(d.split(": ")[1]) for d in data[0]}
        rules['8'] = Rule('42 | 42 8')  # any number of 42
        rules['11'] = Rule('42 31 | 42 31 11')  # any number of 42 31
        # print(rules['0'].match('babbbbaabbbbbabbbbbbaabaaabaaa', 0, rules, d='0'))
        matches = [d for d in data[1] if rules['0'].match(d, 0, rules) == len(d)]
        print(matches)
        answer = len(matches)
        print(f"part 2: {answer}")


def example():
    inp = ['0: 4 1 5',
           '1: 2 3 | 3 2',
             '2: 4 4 | 5 5',
             '3: 4 5 | 5 4',
             '4: "a"',
             '5: "b"']
    rules = rulebook(inp)



if __name__ == "__main__":
    # rules = {'0': Rule('0 1 | 2'), '1': Rule('"a"'), '2': Rule('"b"')}
    # print(rules['0'].match('ab', 0, rules))
    #example()
    #part1()
    part2()  # 275 too low

