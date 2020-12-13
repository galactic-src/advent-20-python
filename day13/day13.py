import math


def first_time(base, route):
    time = route - (base % route)
    return 0 if time == route else time


def part1():
    with open('./input.txt', 'r') as f:
        ts, routes = f.readlines()
        base = int(ts)
        routes = map(int, filter(lambda r: r != 'x', routes.split(',')))
        times = sorted({r: first_time(base, r) for r in routes}.items(), key=lambda el: el[1])
        print(f"part 1: {math.prod(times[0])}")


def part2():
    with open('./input.txt', 'r') as f:
        base, routes = f.readlines()
        routes = [(ix, int(c)) for ix, c in enumerate(routes.split(',')) if c != 'x']
        routes.sort(key=lambda el: el[1], reverse=True)
        step = 1
        candidate = int(base)
        offset, route = routes.pop()
        while True:
            if (candidate + offset) % route == 0:
                if len(routes) == 0:
                    break
                else:
                    step *= route
                    offset, route = routes.pop()
            else:
                candidate += step
        print(f"part 2: {candidate}")


if __name__ == "__main__":
    part1()
    part2()

