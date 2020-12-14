import collections
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, p


def mask_val(mask, val):
    return int("".join([v if m == 'X' else m for m, v in zip(mask, val)]), 2)


def bits(i):
    return f"{int(i):036b}"


class Instruction:
    def __init__(self, s):
        op, arg = s.split(' = ')
        if op.startswith('mem'):
            self.type = 'mem'
            self.addr = int(op[4:].rstrip(']'))
            self.val = arg
        elif op.startswith('mask'):
            self.type = 'mask'
            self.mask = arg


def part1():
    with ManyLineInput('./input.txt', Instruction) as data:
        mask = None
        mem = dict()
        for i in data:
            if i.type == 'mem':
                mem[i.addr] = mask_val(mask, bits(i.val))
            else:
                mask = i.mask
        print(f"part 1: {sum(mem.values())}")


def make_mask(var_indices, c, one_indices):
    mask = list('X' * 36)
    for i in var_indices:
        if i in c:
            mask[i] = '1'
        else:
            mask[i] = '0'
    for i in one_indices:
        mask[i] = '1'
    return "".join(mask)


def all_combinations(var_indices, one_indices):
    for n in range(len(var_indices)+1):
        for c in combinations(var_indices, n):
            yield make_mask(var_indices, c, one_indices)


def mask_val_2(mask, addr):
    var_indices = [ix for ix in range(len(mask)) if mask[ix] == 'X']
    one_indices = [ix for ix in range(len(mask)) if mask[ix] == '1']
    return [mask_val(new_mask, addr) for new_mask in all_combinations(var_indices, one_indices)]


def part2():
    with ManyLineInput('./input.txt', Instruction) as data:
        mask = None
        mem = dict()
        for i in data:
            if i.type == 'mem':
                for addr in mask_val_2(mask, bits(i.addr)):
                    mem[addr] = int(i.val)
            else:
                mask = i.mask
        print(f"part 2: {sum(mem.values())}")




if __name__ == "__main__":
    part1()
    part2()  # 3902437431435 too high

