import collections
from enum import Enum, auto
import hashlib
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput


def valid_numbers(key, md5_prefix):
    n = 1
    while True:
        if useful_hash(key, n, md5_prefix):
            yield n
        n += 1


def useful_hash(key, number, md5_prefix):
    num_bytes = str.encode(repr(number))
    return hashlib.md5(key + num_bytes).hexdigest()[:len(md5_prefix)] == md5_prefix


def first_matching(key, md5_prefix):
    return next(valid_numbers(key, md5_prefix))


def part1():
    print(first_matching(b'ckczppom', '00000'))


def part2():
    print(first_matching(b'ckczppom', '000000'))


if __name__ == "__main__":
    part1()
    part2()

