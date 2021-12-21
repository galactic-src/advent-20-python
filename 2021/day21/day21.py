from collections import namedtuple
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, DelimitedLinesBlockInput
from functools import lru_cache


class DeterministicDie:
    def __init__(self):
        self.rolls = 0

    def roll(self):
        value = self.rolls % 100 + 1
        self.rolls += 1
        return value


class Game:
    def __init__(self, p1_start, p2_start, target, die):
        self.p1_turn = True
        self.p1 = p1_start
        self.p2 = p2_start
        self.target = target
        self.p1_score = 0
        self.p2_score = 0
        self.die = die

    def take_turn(self):
        rolled = 0
        for _ in range(3):
            rolled += self.die.roll()
        if self.p1_turn:
            self.p1 = ((self.p1 + rolled - 1) % 10) + 1
            self.p1_score += self.p1
            self.p1_turn = False
        else:
            self.p2 = ((self.p2 + rolled - 1) % 10) + 1
            self.p2_score += self.p2
            self.p1_turn = True

    def is_finished(self):
        return self.p1_score >= self.target or self.p2_score >= 1000


def part1():
    game = Game(7, 4, 1000, DeterministicDie())
    while not game.is_finished():
        # print(f"{game.p1}, {game.p2}, ({game.p1_score}, {game.p2_score})")
        game.take_turn()

    losing_score = min(game.p1_score, game.p2_score)
    print(f"answer = {losing_score} * {game.die.rolls}")
    answer = losing_score * game.die.rolls
    print(f"part 1: {answer}")


@lru_cache(maxsize=None)
def scores(p1_in, p2_in, p1_score_in, p2_score_in, p1_turn_in, roll_number_in):
    p1 = p1_in
    p2 = p2_in
    p1_score = p1_score_in
    p2_score = p2_score_in
    p1_turn = p1_turn_in
    roll_number = roll_number_in
    print(f"scores {p1}, {p2}, {p1_score}, {p2_score}, {p1_turn}, {roll_number}")

    if p1_score >= 21:
        print(f"calculated: {p1_in}, {p2_in}, {p1_score_in}, {p2_score_in}, {p1_turn_in}, {roll_number_in}, {[1,0]}")
        return [1, 0]
    elif p2_score >= 21:
        print(f"calculated: {p1_in}, {p2_in}, {p1_score_in}, {p2_score_in}, {p1_turn_in}, {roll_number_in}, {[0,1]}")
        return [0, 1]

    results = [0, 0]
    for roll in range(1, 4):
        if p1_turn:
            p1 = ((p1 + roll - 1) % 10) + 1
            if roll_number == 2:
                p1_score += p1
        else:
            p2 = ((p2 + roll - 1) % 10) + 1
            if roll_number == 2:
                p2_score += p2

        if roll_number == 2:
            roll_number = 0
            p1_turn = not p1_turn
        else:
            roll_number += 1

        p1_wins, p2_wins = scores(p1, p2, p1_score, p2_score, p1_turn, roll_number)
        results[0] += p1_wins
        results[1] += p2_wins

    print(f"calculated: {p1_in}, {p2_in}, {p1_score_in}, {p2_score_in}, {p1_turn_in}, {roll_number_in}, {results}")
    return results


def part2():
    results = scores(4, 8, 0, 0, True, 0)

    answer = max(results)
    print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()