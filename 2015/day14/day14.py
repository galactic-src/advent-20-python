from collections import Counter
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


class Reindeer:
    def __init__(self, s):
        self.name, remainder = s.split(' can fly ')
        speed, remainder = remainder.split(' km/s for ')
        self.speed = int(speed)
        fly_time, remainder = remainder.split(' seconds, but then must rest for ')
        self.fly_time = int(fly_time)
        rest_time, _ = remainder.split(' seconds.')
        self.rest_time = int(rest_time)

    def distance_after(self, time):
        whole_cycles = time // (self.fly_time + self.rest_time)
        remainder = min(self.fly_time, time % (self.fly_time + self.rest_time))
        return (whole_cycles * self.fly_time + remainder) * self.speed


class Race:
    def __init__(self, reindeers, time):
        self.reindeers = reindeers
        self.time = time

    def results(self):
        return {reindeer.name: reindeer.distance_after(self.time) for reindeer in self.reindeers}

    def winning_distance(self):
        return max(self.results().values())

    def winners(self):
        max_distance = max(map(lambda res: res[1], self.results().items()))
        return [res[0] for res in self.results().items() if res[1] == max_distance]


def part1():
    with ManyLineInput('./input.txt', Reindeer) as data:
        answer = Race(data, 2503).winning_distance()
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', Reindeer) as data:
        winners = [winner for t in range(1, 2503 + 2) for winner in Race(data, t).winners()]
        c = Counter(winners)
        answer = max(c.values())
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()  # not 87, 647, 648 (low)
