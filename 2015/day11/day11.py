import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed


def inc(num, ix):
    c = num[ix]
    if c == 'z':
        num[ix] = 'a'
        inc(num, ix-1)
    elif chr(ord(c) + 1) in 'iol':
        for i in range(ix+1, len(num)-1):
            num[i] = 'a'
        num[ix] = chr(ord(c) + 2)
    else:
        num[ix] = chr(ord(c) + 1)


def next_pwd(prev):
    inc(prev, len(prev)-1)
    return prev


def pwds(p):
    for ix, c in enumerate(p):
        if c in "iol":
            for i in range(ix+1, len(p)-1):
                p[i] = 'a'
            p[ix] = chr(ord(c) + 1)

    while True:
        p = next_pwd(p)
        yield list(p)


def got_straight(p):
    return any(map(lambda w: ord(w[0])+1 == ord(w[1]) and ord(w[1])+1 == ord(w[2]), windowed(p, 3)))


def got_two_pairs(p):
    found = False
    prev = None
    for c in p:
        if prev == c:
            if found:
                return True
            else:
                found = True
                prev = None
        else:
            prev = c
    else:
        return False


def is_valid(p):
    return got_straight(p) and got_two_pairs(p)


def solve():
    prev = list('vzbxkghb')
    answer = "".join(next(filter(is_valid, pwds(prev))))
    print(f"part 1: {answer}")
    answer = "".join(next(filter(is_valid, pwds(list(answer)))))
    print(f"part 2: {answer}")


if __name__ == "__main__":
    solve()

