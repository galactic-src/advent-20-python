from itertools import tee
from more_itertools import split_at


class OneLineInput:
    def __init__(self, input_path):
        self.input_path = input_path
        self.file = None

    def __enter__(self):
        self.file = open(self.input_path)
        self.file.__enter__()
        lines = self.file.readlines()
        if len(lines) != 1:
            raise Exception(f'expected single line, found {len(lines)}')
        return lines[0]

    def __exit__(self, exc_type, value, traceback):
        self.file.__exit__(exc_type, value, traceback)


class ManyLineInput:
    def __init__(self, input_path, cons=None):
        self.input_path = input_path
        self.file = None
        self.cons = cons

    def __enter__(self):
        self.file = open(self.input_path)
        self.file.__enter__()
        lines = self.file.readlines()
        if self.cons is None:
            return [s.rstrip('\n') for s in lines]
        else:
            return [self.cons(s.rstrip('\n')) for s in lines]

    def __exit__(self, exc_type, value, traceback):
        self.file.__exit__(exc_type, value, traceback)


class DelimitedLinesBlockInput:
    def __init__(self, input_path, cons=None):
        self.input_path = input_path
        self.file = None
        self.cons = cons

    def __enter__(self):
        self.file = open(self.input_path)
        self.file.__enter__()
        lines = self.file.readlines()
        blocks = list(split_at([s.rstrip('\n') for s in lines], lambda l: l == ""))
        return blocks if self.cons is None else map(lambda b: self.cons(b), blocks)

    def __exit__(self, exc_type, value, traceback):
        self.file.__exit__(exc_type, value, traceback)


def windowed(iterable, size):
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each, None)
    return zip(*iters)


def partitions(n, total):
    if n == 1:
        yield (total,)
    else:
        for num in range(total+1):
            for partition in [(num, *p) for p in partitions(n-1, total-num)]:
                yield partition


def p(o):
    print(o)
    return o


def plist(o):
    return p(list(o))


def first(cond, it):
    return next(filter(cond, it))
