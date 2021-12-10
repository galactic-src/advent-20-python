from collections import Counter

from util import ManyLineInput

pairs = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

illegalPoints = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

autoPoints = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}


def first_illegal(s):
    stack = []
    for c in s:
        if c in pairs.keys():
            stack.append(c)
        elif c in pairs.values():
            opener = stack.pop()
            if c != pairs[opener]:
                return c
    return None


def autocomplete_score(s):
    stack = []
    for c in s:
        if c in pairs.keys():
            stack.append(c)
        elif c in pairs.values():
            opener = stack.pop()
            if c != pairs[opener]:
                raise Exception("oops")

    score = 0
    for opener in stack[::-1]:
        score *= 5
        score += autoPoints[opener]

    return score


def part1():
    with ManyLineInput('./input.txt') as data:
        c = Counter(first_illegal(s) for s in data)
        total = sum(c[close] * illegalPoints[close] for close in illegalPoints.keys())
        print(f"part 1: {total}")


def part2():
    with ManyLineInput('./input.txt') as data:
        scores = sorted([autocomplete_score(s) for s in data if first_illegal(s) is None])

        answer = scores[len(scores)//2]
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

