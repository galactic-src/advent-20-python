from util import ManyLineInput


def sum_pow2(s, on):
    return sum(map(lambda ic: pow(2, len(s) - ic[0] - 1) * int(ic[1] == on), enumerate(s)))


class BoardingPass:
    def __init__(self, s):
        self.row = sum_pow2(s[:7], 'B')
        self.col = sum_pow2(s[7:], 'R')

    def seat_id(self):
        return 8 * self.row + self.col


def part1():
    with ManyLineInput('./input.txt', BoardingPass) as data:
        answer = max(map(lambda bp: bp.seat_id(), data))
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', BoardingPass) as data:
        seat_ids = {bp.seat_id() for bp in data}
        answer = set(range(min(seat_ids),  max(seat_ids))) - seat_ids
        print(f"part 2: {list(answer)[0]}")


if __name__ == "__main__":
    part1()
    part2()

