from enum import Enum, auto

from util import ManyLineInput


class Exploded(Exception):
    pass


class Splitted(Exception):
    pass


class FinishedReducing(Exception):
    pass


class Leaf:
    def __init__(self, value):
        self.value = value
        self.before = None
        self.after = None
        self.parent = None

    def magnitude(self):
        return self.value

    def print_string(self):
        return f"{self.value}"


class Pair:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def print_string(self):
        return f"[{self.left.print_string()},{self.right.print_string()}]"

    def set_left(self, node):
        self.left = node
        node.parent = self

    def set_right(self, node):
        self.right = node
        node.parent = self


class SFNumber:
    def __init__(self):
        self.root = None
        self.leaves = Leaf(None)

    def magnitude(self):
        return self.root.magnitude()

    def add(self, other):
        sentinel = self.leaves
        while sentinel.after:
            sentinel = sentinel.after
        last_leaf = sentinel.before
        other_first = other.leaves.after
        last_leaf.after = other_first
        other_first.before = last_leaf

        new_root = Pair()
        new_root.left = self.root
        self.root.parent = new_root
        new_root.right = other.root
        other.root.parent = new_root
        self.root = new_root

        self.reduce()

    def reduce(self):
        try:
            while True:
                try:
                    self.reduce_explode(self.root, 1)
                    self.reduce_split(self.leaves)
                    raise FinishedReducing()

                except Exploded:
                    pass
                except Splitted:
                    pass
                self.sanity_check()
        except FinishedReducing:
            pass

    def reduce_explode(self, pair, depth):
        if isinstance(pair.left, Leaf) and isinstance(pair.right, Leaf) and depth > 4:
            before_pair = pair.left.before
            after_pair = pair.right.after
            if before_pair is not None and before_pair.value is not None:
                before_pair.value += pair.left.value
            if after_pair is not None and after_pair.value is not None:
                after_pair.value += pair.right.value

            new_leaf = Leaf(0)
            self.wire_up(before_pair, new_leaf)
            self.wire_up(new_leaf, after_pair)

            if pair.parent:
                new_leaf.parent = pair.parent
                if pair.parent.left is pair:
                    pair.parent.left = new_leaf
                elif pair.parent.right is pair:
                    pair.parent.right = new_leaf
                else:
                    raise Exception("oops")
            raise Exploded()
        else:
            if isinstance(pair.left, Pair):
                self.reduce_explode(pair.left, depth+1)
            if isinstance(pair.right, Pair):
                self.reduce_explode(pair.right, depth+1)

    def reduce_split(self, leaf):
        while leaf.after is not None:
            if leaf.value is not None and leaf.value >= 10:
                new_pair = Pair()
                new_pair.parent = leaf.parent

                new_pair.set_left(Leaf(leaf.value // 2))
                new_pair.set_right(Leaf((leaf.value + 1) // 2))

                if leaf.parent.left is leaf:
                    leaf.parent.left = new_pair
                elif leaf.parent.right is leaf:
                    leaf.parent.right = new_pair
                else:
                    raise Exception("oops")

                self.wire_up(leaf.before, new_pair.left)
                self.wire_up(new_pair.left, new_pair.right)
                self.wire_up(new_pair.right, leaf.after)

                raise Splitted()

            leaf = leaf.after

    def wire_up(self, first, second):
        first.after = second
        second.before = first

    def __str__(self):
        return self.root.print_string()

    def all_leaves(self):
        leaf = self.leaves
        yield leaf
        while leaf.after:
            leaf = leaf.after
            yield leaf

    def sanity_check(self):
        self.sanity_check_tree(self.root)
        self.sanity_check_leaves()

    def sanity_check_tree(self, p):
        if p.parent is None and p is not self.root:
            raise Exception("node without parent")

        if isinstance(p, Pair):
            if p.left.parent is not p:
                raise Exception("pair parent wrong")
            if p.right.parent is not p:
                raise Exception("pair parent wrong")
            self.sanity_check_tree(p.left)
            self.sanity_check_tree(p.right)
        if isinstance(p, Leaf):
            if p.value is None:
                raise Exception("leaf without value")

    def sanity_check_leaves(self):
        last_leaf = self.leaves
        leaf = last_leaf.after
        while True:
            if leaf.before is not last_leaf:
                raise Exception("leaves not wired up")

            if leaf.after is None:
                break
            last_leaf = leaf
            leaf = last_leaf.after


class PState(Enum):
    START = auto()
    LHS = auto()
    RHS = auto()
    FINISHED = auto()


class SFParser:
    def __init__(self):
        self.number = None
        self.pair = None
        self.leaf = None
        self.state = PState.START
        self.value = ""

    def parse(self, s):
        for c in s:
            if self.state == PState.FINISHED:
                raise Exception(f"finished, but {c}")
            if c == '[':
                self.handle_open()
            elif c == ']':
                self.handle_right_finished()
            elif c == ',':
                self.handle_left_finished()
            elif c.isdigit():
                self.value += c
            else:
                raise Exception(f"parse {c}")

        if self.state != PState.FINISHED:
            raise Exception("not finished")

        return self.number

    def handle_open(self):
        new_pair = Pair()
        if self.state == PState.START:
            self.number = SFNumber()
            self.number.root = new_pair
            self.leaf = self.number.leaves
        elif self.state == PState.LHS:
            self.pair.left = new_pair
            new_pair.parent = self.pair
        elif self.state == PState.RHS:
            self.pair.right = new_pair
            new_pair.parent = self.pair

        self.pair = new_pair
        self.state = PState.LHS

    def handle_right_finished(self):
        if self.value and self.pair.right:
            raise Exception("value but right is already set")
        if not self.value and not self.pair.right:
            raise Exception("no value and right is unset")

        if self.value:
            self.pair.right = self._add_leaf()
            self.pair.right.parent = self.pair

        if self.pair.parent:
            self.pair = self.pair.parent
            self.state = PState.RHS
        else:
            self._add_leaf()
            self.state = PState.FINISHED

    def handle_left_finished(self):
        if self.value and self.pair.left:
            raise Exception("value but left is already set")
        if not self.value and not self.pair.left:
            raise Exception("no value and left is unset")

        if self.value:
            self.pair.left = self._add_leaf()
            self.pair.left.parent = self.pair

        self.state = PState.RHS

    def _add_leaf(self):
        leaf = Leaf(int(self.value)) if self.value else Leaf(None)
        self.value = ""
        leaf.before = self.leaf
        self.leaf.after = leaf
        self.leaf = leaf
        return leaf


def part1():
    with ManyLineInput('./input.txt') as data:
        numbers = [SFParser().parse(line) for line in data]

        n = numbers[0]
        for other in numbers[1:]:
            n.add(other)
        print(f"part 1: {n.magnitude()}")


def part2():
    with ManyLineInput('./input.txt') as data:
        max_magnitude = 0
        for ix1 in range(len(data)):
            for ix2 in range(len(data)):
                if ix1 != ix2:
                    n1 = SFParser().parse(data[ix1])
                    n2 = SFParser().parse(data[ix2])
                    n1.add(n2)
                    max_magnitude = max(n1.magnitude(), max_magnitude)

        print(f"part 2: {max_magnitude}")


if __name__ == "__main__":
    part1()
    part2()
