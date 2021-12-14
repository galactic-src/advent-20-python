from util import DelimitedLinesBlockInput


def parse_point(line):
    x, y = line.split(',')
    return int(x), int(y)


def parse_fold(line):
    axis, level = line.lstrip('fold along ').split('=')
    return axis, int(level)


class OrigamiSheet:
    def __init__(self, data):
        self.points = {parse_point(line) for line in data[0]}
        self.folds = [parse_fold(line) for line in data[1]]

    def width(self):
        return max(x for x, _y in self.points)

    def height(self):
        return max(y for _x, y in self.points)

    def print(self):
        grid = [['.'] * (self.width()+1) for _ in range(self.height()+1)]
        for x, y in self.points:
            grid[y][x] = '#'
        for row in grid:
            print(''.join(row))

    def fold(self, axis, level):
        new_points = set()
        if axis == 'x':
            adjust = min(2 * level - self.width(), 0)
            for x, y in self.points:
                if x <= level:
                    new_points.add((x - adjust, y))
                else:
                    new_points.add((level - (x - level) - adjust, y))
        else:
            adjust = min(2 * level - self.height(), 0)
            for x, y in self.points:
                if y <= level:
                    new_points.add((x, y - adjust))
                else:
                    new_points.add((x, level - (y - level) - adjust))

        self.points = new_points

    def visible_points(self):
        return len(self.points)


def part1():
    with DelimitedLinesBlockInput('./input.txt') as data:
        sheet = OrigamiSheet(data)
        axis, level = sheet.folds[0]
        sheet.fold(axis, level)

        print(f"part 1: {sheet.visible_points()}")


def part2():
    with DelimitedLinesBlockInput('./input.txt') as data:
        sheet = OrigamiSheet(data)
        for axis, level in sheet.folds:
            sheet.fold(axis, level)
        print("part 2:")
        sheet.print()


if __name__ == "__main__":
    part1()
    part2()
