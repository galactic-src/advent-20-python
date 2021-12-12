from util import ManyLineInput


adjacent = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


def with_border(lines, border_val):
    width = len(lines[0])
    return ([(width + 2) * [border_val]]
            + [[border_val] + [int(energy) for energy in line] + [border_val] for line in lines]
            + [(width + 2) * [border_val]])


class Grid:
    def __init__(self, verbose):
        self.verbose = verbose
        self.step_num = 0
        with ManyLineInput('./input.txt') as data:
            self.grid = with_border(data, 0)

    def print(self):
        for line in self.grid[1:-1]:
            print(''.join([str(energy) for energy in line[1:-1]]))
        print("\n")

    def flash_one(self, flashed):
        for y in range(1, len(self.grid) - 1):
            for x in range(1, len(self.grid[0]) - 1):
                if (x, y) not in flashed and self.grid[y][x] > 9:
                    for adjX, adjY in [(x + diffX, y + diffY) for diffX, diffY in adjacent]:
                        self.grid[adjY][adjX] += 1
                    flashed.add((x, y))
                    return True
        else:
            return False

    def step(self):
        for y in range(1, len(self.grid) - 1):
            for x in range(1, len(self.grid[0]) - 1):
                self.grid[y][x] += 1

        flashed = set()
        while self.flash_one(flashed):
            pass

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] > 9:
                    self.grid[y][x] = 0

        self.step_num += 1
        return len(flashed)

    def size(self):
        return (len(self.grid) - 2) * (len(self.grid[0]) - 2)


def part1():
    grid = Grid(False)

    flashes = 0
    for stepNum in range(100):
        flashed = grid.step()
        flashes += flashed
        print(f"STEP {grid.step_num}")
        grid.print()

    print(f"part 1: {flashes}")


def part2():
    grid = Grid(False)

    while True:
        flashed = grid.step()
        if flashed == grid.size():
            break

    print(f"part 2: {grid.step_num}")


if __name__ == "__main__":
    part1()
    part2()
