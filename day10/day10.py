import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


# charging outlet 0, device built-in max+3
# input can be 1-3 below, and gives output joltage

def part1():
    with ManyLineInput('./input.txt', int) as data:
        socket = 0
        inbuilt = max(data) + 3
        counter = collections.Counter(map(lambda w: w[1] - w[0], windowed(sorted(data + [socket, inbuilt]), 2)))
        answer = counter[1] * counter[3]
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', int) as data:
        socket = 0
        inbuilt = max(data) + 3
        data = list(sorted(data + [socket, inbuilt]))
        dag = {}
        for n in data:
            dag[n] = []
            for m in range(1, 4):
                if n+m in data:
                    dag[n].append(n+m)

        routes_to_end = {}
        for k in data[::-1]:
            routes_to_end[k] = max(1, sum(routes_to_end[i] for i in dag[k]))

        answer = routes_to_end[0]
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

