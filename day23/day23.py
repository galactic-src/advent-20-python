import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


class Game:
    def __init__(self, s, extra=[]):
        self.cards = [int(c) for c in s] + extra
        self.prev_cards = [c for c in self.cards]
        self.current = self.cards[0]

    def pop3(self):
        return [self.pop1(), self.pop1(), self.pop1()]

    def pop1(self):
        ix = self.cards.index(self.current)
        if ix < len(self.cards)-1:
            return self.cards.pop(ix+1)
        else:
            return self.cards.pop(0)

    def find_dest(self):
        target = self.current-1
        while True:
            if target == 0:
                return max(self.cards)
            if target in self.cards:
                return target
            target -= 1

    def take_turn(self):
        to_move = self.pop3()
        dest = self.find_dest()
        dest_ix = self.cards.index(dest)

        tmp_cards = self.cards
        self.cards = self.prev_cards
        self.prev_cards = tmp_cards

        ix = 0
        for c in self.prev_cards[:dest_ix+1]:
            self.cards[ix] = c
            ix += 1
        for c in to_move:
            self.cards[ix] = c
            ix += 1
        for c in self.prev_cards[dest_ix+1:]:
            self.cards[ix] = c
            ix += 1
        self.current = self.cards[(self.cards.index(self.current)+1)%len(self.cards)]
        self.prev_cards.extend(to_move)


INPUT = '158937462'
EXAMPLE = '389125467'


def from1(cards):
    ix = cards.index(1)
    if ix == 0:
        rotated = cards[1:]
    elif ix == len(cards)-1:
        rotated = cards[:-1]
    else:
        rotated = cards[ix+1:] + cards[:ix]
    return "".join([str(i) for i in rotated])


def part1():
    game = Game(INPUT)
    for turn in range(100):
        game.take_turn()
    answer = from1(game.cards)
    print(f"part 1: {answer}")


def part2():
    game = Game(INPUT, list(range(10, 1000001)))
    for turn in range(10000000):
        print(turn)
        game.take_turn()
    ix = game.cards.index(1)
    answer = game.cards[ix+1] * game.cards[ix+2]
    print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()


