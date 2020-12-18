
from util import ManyLineInput, OneLineInput, windowed, p


def find_outside_brackets(expr, token):
    ix = 0
    br = 0
    while ix < len(expr):
        c = expr[ix]

        if c == '(':
            br += 1
        elif c == ')':
            br -= 1
        elif br == 0 and c == token:
            return ix
        ix += 1
    else:
        return None


def parse(expr):
    if expr[0] == '(' and find_closing(expr, 0) == (len(expr)-1):
        return parse(expr[1:-1])
    if len(expr) == 1:
        return Num(expr)
    elif ix := find_outside_brackets(expr, '*'):
        return Op('*', expr[:ix], expr[ix+1:])
    elif ix := find_outside_brackets(expr, '+'):
        return Op('+', expr[:ix], expr[ix+1:])
    else:
        raise Exception(f"parse {expr}")


def evaluate2(tree):
    if isinstance(tree, Num):
        return tree.val
    elif isinstance(tree, Op):
        if tree.op == '*':
            return evaluate2(tree.lhs) * evaluate2(tree.rhs)
        elif tree.op == '+':
            return evaluate2(tree.lhs) + evaluate2(tree.rhs)
    else:
        raise Exception('evaluate2')


class Num:
    def __init__(self, val):
        self.val = int(val)


class Op:
    def __init__(self, op, lhs, rhs):
        self.op = op
        self.lhs = parse(lhs)
        self.rhs = parse(rhs)


def find_closing(expr, start):
    ix = start
    br = 0
    while ix < len(expr):
        if expr[ix] == '(':
            br += 1
        elif expr[ix] == ')':
            br -= 1
            if br == 0:
                return ix
        ix += 1


def read_num(e, ix):
    if e[ix] == '(':
        closing = find_closing(e,ix)
        sub = e[ix+1:closing]
        return evaluate(sub), closing+1
    else:
        return int(e[ix]), ix + 1


def evaluate(e):
    ix = 0
    result, ix = read_num(e, ix)
    while ix < len(e):
        op = e[ix]
        rhs, ix = read_num(e, ix+1)
        if op == '+':
            result += rhs
        elif op == '*':
            result *= rhs
    return result


def part1():
    with ManyLineInput('./input.txt') as data:
        answer = sum(evaluate(expr.replace(" ", "")) for expr in data)
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt') as data:
        answer = sum(evaluate2(parse(expr.replace(" ", ""))) for expr in data)
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
