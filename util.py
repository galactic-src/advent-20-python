from itertools import tee

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


def windowed(iterable, size):
    iters = tee(iterable, size)
    for i in range(1, size):
        for each in iters[i:]:
            next(each, None)
    return zip(*iters)
