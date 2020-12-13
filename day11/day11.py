import collections
import numpy as np
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed

FLOOR = '.'
UNOCCUPIED = 'L'
OCCUPIED = '#'
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def seat(occ):
    if occ is True:
        return OCCUPIED
    elif occ is False:
        return UNOCCUPIED
    else:
        return FLOOR


class Ferry:
    def __init__(self, data, line_of_sight, threshold):
        self.h = len(data)
        self.w = len(data[0])
        self.adjacent_seats = self.line_of_sight_seats(data) if line_of_sight else self.build_adjacent_seats(data)
        # print(self.adjacent_seats)
        self.occupied = [[None for _ in range(self.w)] for _ in range(self.h)]
        for h, row in enumerate(data):
            for w, letter in enumerate(row):
                if letter == UNOCCUPIED:
                    self.occupied[h][w] = False
        # print(self.occupied)
        self.steps = 0
        self.threshold =threshold

    def build_adjacent_seats(self, data):
        return [[[(h+v[1], w+v[0]) for v in DIRECTIONS
                if data[h][w] == UNOCCUPIED and 0 <= h + v[1] < self.h and 0 <= w + v[0] < self.w and data[h+v[1]][w+v[0]] == UNOCCUPIED]
                for w in range(self.w)] for h in range(self.h)]

    def first_in_direction(self, h, w, v, data):
        #if h==0:
        #    print(f"first_in_direction from ({h}, {w}) in direction {v}")
        while 0 <= h + v[1] < self.h and 0 <= w + v[0] < self.w:
            h1 = h+v[1]
            w1 = w+v[0]
            #if h==0:
            #    print(f"check ({h1},{w1})")
            if data[h1][w1] == UNOCCUPIED:
                #if h==0:
                #   print("yep")
                return h1, w1
            h = h1
            w = w1
        return None

    def los_adj(self, data, h, w):
        #if h==0:
        #    print(f"los_adj ({h},{w})")
        if data[h][w] == FLOOR:
            return []
        else:
            return list(filter(None, (self.first_in_direction(h, w, v, data) for v in DIRECTIONS)))

    def line_of_sight_seats(self, data):
        return [[self.los_adj(data, h, w) for w, c in enumerate(row)] for h, row in enumerate(data)]

    def go(self):
        while self.step():
            # self.print_state()
            self.steps += 1
            # print(self.steps)
        self.steps -= 1

    def step(self):
        changed = False
        occ_next = [[state for state in row] for row in self.occupied]
        for h, row in enumerate(self.occupied):
            for w, occupied in enumerate(row):
                # print(self.adjacent_seats[h][w])
                # print(list(self.occupied[h][w] is True for h, w in self.adjacent_seats[h][w]))
                adj_occ = sum(self.occupied[h][w] is True for h, w in self.adjacent_seats[h][w])
                # print(f"({h},{w}) - {occupied} - {adj_occ}")
                if occupied is True:
                    if adj_occ >= self.threshold:
                        changed = True
                        occ_next[h][w] = False
                elif occupied is False:
                    if adj_occ == 0:
                        changed = True
                        occ_next[h][w] = True
        # print(occ_next)
        self.occupied = occ_next
        return changed

    def passengers(self):
        return sum(o is True for row in self.occupied for o in row)

    def print_state(self):
        for row in self.occupied:
            print("".join(map(seat, row)))
        print("")


def part1():
    with ManyLineInput('./input.txt') as data:
        # print(data)
        ferry = Ferry(data, False, 4)
        # ferry.print_state()
        ferry.go()
        answer = ferry.passengers()
        print(f"part 1: {answer} after {ferry.steps} steps")


def part2():
    with ManyLineInput('./input.txt') as data:
        ferry = Ferry(data, True, 5)
        # ferry.print_state()
        ferry.go()
        answer = ferry.passengers()
        print(f"part 2: {answer} after {ferry.steps} steps")


if __name__ == "__main__":
    # part1()
    part2()

