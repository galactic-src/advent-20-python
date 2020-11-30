import re
from itertools import combinations

from util import ManyLineInput


class Box:
    expr = re.compile("(\d+)x(\d+)x(\d+)")

    def __init__(self, input):
        m = Box.expr.fullmatch(input)
        dims = sorted(map(int, m.groups()))
        self.l, self.w, self.h = dims

    def surface(self):
        return 2 * sum(map(lambda x: x[0] * x[1], list(combinations([self.l, self.w, self.h], 2))))

    def smallest_face(self):
        return self.l * self.w

    def total_paper(self):
        return self.surface() + self.smallest_face()

    def smallest_perimeter(self):
        return 2 * (self.l + self.w)

    def volume(self):
        return self.l * self.w * self.h

    def total_ribbon(self):
        return self.volume() + self.smallest_perimeter()


def part1():
    with ManyLineInput('./input.txt', Box) as data:
        total_paper = sum(map(Box.total_paper, data))
        print(f"part 1: {total_paper}")


def part2():
    with ManyLineInput('./input.txt', Box) as data:
        total_ribbon = sum(map(Box.total_ribbon, data))
        print(f"part 2: {total_ribbon}")


if __name__ == "__main__":
    part1()
    part2()
