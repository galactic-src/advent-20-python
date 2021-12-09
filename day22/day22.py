import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, DelimitedLinesBlockInput

def parse_player(lines):
    return Player([int(l) for l in lines[1:]])

class Player:
    def __init__(self, cards):
        self.cards = cards


class RecursiveGame:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.rounds = []
        self.winner = None

    def play_round(self):
        if self.winner:
            raise Exception(f"{self.winner} already won")

        if [self.p1.cards, self.p2.cards] in self.rounds:
            self.winner = 'p1'
        else:
            self.rounds.append([list(self.p1.cards), list(self.p2.cards)])

        c1 = self.p1.cards.pop(0)
        c2 = self.p2.cards.pop(0)
        if len(self.p1.cards) < c1 or len(self.p2.cards) < c2:
        else:
            self.winner = 'p1' if c1 > c2 else 'p2'



def part1():
    with DelimitedLinesBlockInput('./input.txt') as data:
        p1 = parse_player(data[0])
        p2 = parse_player(data[1])

        while p1.cards and p2.cards:
            c1 = p1.cards.pop(0)
            c2 = p2.cards.pop(0)
            if c1 > c2:
                p1.cards.append(c1)
                p1.cards.append(c2)
            else:
                p2.cards.append(c2)
                p2.cards.append(c1)

        winner = p1 if len(p1.cards) > 0 else p2
        answer = sum((ix+1) * c for ix, c in enumerate(winner.cards[::-1]))
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt') as data:
    # with OneLineInput('./day23.py') as data:
        answer = ''
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    # part2()

