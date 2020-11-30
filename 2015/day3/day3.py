import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput


class Direction(Enum):
    UP = auto(),
    DOWN = auto(),
    LEFT = auto(),
    RIGHT = auto()


Location = collections.namedtuple('Location', 'x y')


def follow(location, direction):
    if direction is Direction.UP:
        return Location(location.x, location.y+1)
    elif direction is Direction.DOWN:
        return Location(location.x, location.y-1)
    elif direction is Direction.LEFT:
        return Location(location.x-1, location.y)
    elif direction is Direction.RIGHT:
        return Location(location.x+1, location.y)


def parse_direction(sym):
    if sym == '^':
        return Direction.UP
    elif sym == 'v':
        return Direction.DOWN
    elif sym == '<':
        return Direction.LEFT
    elif sym == '>':
        return Direction.RIGHT
    else:
        raise ValueError(f"unexpected direction token {sym}")


def locations_visited(data):
    return accumulate(map(parse_direction, data), follow, initial=Location(x=0, y=0))


def unique_locations_visited(data):
    return set(locations_visited(data))


def count_locations_visited(data):
    return len(unique_locations_visited(data))


def part1():
    with OneLineInput('./input.txt') as data:
        print(f"part 1: {count_locations_visited(data)}")


def part2():
    with OneLineInput('./input.txt') as data:
        santa_visited = unique_locations_visited(data[::2])
        robo_visited = unique_locations_visited(data[1::2])
        print(f"part 2: {len(santa_visited.union(robo_visited))}")


if __name__ == "__main__":
    part1()  # 2592
    part2()
