from util import ManyLineInput

ACTIVE='#'
INACTIVE='.'


def step(game_state):
    xs, ys, zs = zip(*game_state)
    xmax = max(xs) + 1
    xmin = min(xs) - 1
    ymax = max(ys) + 1
    ymin = min(ys) - 1
    zmax = max(zs) + 1
    zmin = min(zs) - 1

    to_remove = set()
    to_add = set()

    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            for z in range(zmin, zmax+1):
                active = (x,y,z) in game_state
                neighbours = 0
                for dx in range(-1,2):
                    for dy in range(-1,2):
                        for dz in range(-1,2):
                            if dx==0 and dy==0 and dz==0:
                                continue
                            if (x+dx, y+dy, z+dz) in game_state:
                                neighbours += 1
                if active and neighbours != 2 and neighbours != 3:
                    to_remove.add((x,y,z))
                elif not active and neighbours == 3:
                    to_add.add((x,y,z))

    game_state -= to_remove
    game_state |= to_add


def step2(game_state):
    xs, ys, zs, ws = zip(*game_state)
    xmax = max(xs) + 1
    xmin = min(xs) - 1
    ymax = max(ys) + 1
    ymin = min(ys) - 1
    zmax = max(zs) + 1
    zmin = min(zs) - 1
    wmax = max(ws) + 1
    wmin = min(ws) - 1

    to_remove = set()
    to_add = set()

    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            for z in range(zmin, zmax+1):
                for w in range(wmin, wmax+1):
                    active = (x,y,z,w) in game_state
                    neighbours = 0
                    for dx in range(-1,2):
                        for dy in range(-1,2):
                            for dz in range(-1,2):
                                for dw in range(-1,2):
                                    if dx==0 and dy==0 and dz==0 and dw==0:
                                        continue
                                    if (x+dx, y+dy, z+dz, w+dw) in game_state:
                                        neighbours += 1
                    if active and neighbours != 2 and neighbours != 3:
                        to_remove.add((x,y,z,w))
                    elif not active and neighbours == 3:
                        to_add.add((x,y,z,w))

    game_state -= to_remove
    game_state |= to_add


def pgame(game_state):
    xs, ys, zs = zip(*game_state)
    xmax = max(xs)
    xmin = min(xs)
    ymax = max(ys)
    ymin = min(ys)
    zmax = max(zs)
    zmin = min(zs)

    lstate = [[['#' if (x,y,z) in game_state else '.' for x in range(xmin,xmax+1)] for y in range(ymin,ymax+1)] for z in range(zmin, zmax+1)]
    for f, floor in enumerate(lstate):
        for row in floor:
            print("".join(row))
        print('')


def part1():
    with ManyLineInput('./input.txt') as data:
        game_state = set()
        for y, row in enumerate(data):
            for x, c in enumerate(row):
                if c == ACTIVE:
                    game_state.add((x, y, 0))
        for s in range(6):
            step(game_state)

        print(f"part 1: {len(game_state)}")


def part2():
    with ManyLineInput('./input.txt') as data:
        game_state = set()
        for y, row in enumerate(data):
            for x, c in enumerate(row):
                if c == ACTIVE:
                    game_state.add((x, y, 0, 0))
        for s in range(6):
            step2(game_state)
        print(f"part 2: {len(game_state)}")


if __name__ == "__main__":
    part1()
    part2()

