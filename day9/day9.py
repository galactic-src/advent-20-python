from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


def first_invalid(numbers):
    invalids = [w[25] for w in windowed(numbers, 26) if w[25] not in {a+b for a, b in combinations(w[:25], 2)}]
    return invalids[0]


def part1():
    with ManyLineInput('./input.txt', int) as data:
        answer = first_invalid(data)
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', int) as data:
        answer = None
        target = first_invalid(data)
        for start_ix in range(len(data)):
            sums = [a for a in accumulate(data[start_ix:]) if a <= target]
            if len(sums) and sums[-1] == target:
                nums = data[start_ix:start_ix+len(sums)]
                answer = max(nums) + min(nums)
                break
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
