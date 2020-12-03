from util import ManyLineInput


class EscapedString:
    def __init__(self, s):
        self.s = s
        self.decoded = eval(s)
        self.escaped = '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def part1():
    with ManyLineInput('./input.txt', EscapedString) as data:
        answer = sum(map(lambda s: len(s.s) - len(s.decoded), data))
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', EscapedString) as data:
        answer = sum(map(lambda s: len(s.escaped) - len(s.s), data))
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
