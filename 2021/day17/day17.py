class NextX(Exception):
    pass


class NextY(Exception):
    pass


def split_coord(s):
    print(s)
    x, y = s.split(',')
    return int(x), int(y)


def solve():
    target_x = (169, 206)
    target_y = (-108, -68)

    velocities = []

    min_x = 0
    while min_x * (min_x + 1) / 2 < target_x[0]:
        min_x += 1
    max_x = target_x[1]

    min_y = target_y[0]
    max_y = -target_y[0] + 10

    best_y = 0

    for try_x in range(min_x, max_x+1):
        try_y = min_y
        best_y_this_flight = 0

        try:
            while True:
                x, y = 0, 0
                ax, ay = -1, -1
                vx, vy = try_x, try_y

                try:
                    while True:
                        x += vx
                        if vx == 0 and ax != 0:
                            ax = 0
                        y += vy
                        best_y_this_flight = max(best_y_this_flight, y)

                        vx += ax
                        vy += ay

                        if target_x[0] <= x <= target_x[1] and target_y[0] <= y <= target_y[1]:
                            best_y = max(best_y_this_flight, best_y)
                            velocities.append((try_x, try_y))
                            raise NextX()

                        if x > target_x[1] and y < target_y[1]:
                            # too far, next x
                            raise NextY()

                        if x < target_x[0] and y < target_y[0]:
                            # too short, next y
                            raise NextX()

                        if y < target_y[0]:
                            raise NextX()

                except NextX:
                    try_y += 1
                    if try_y > max_y:
                        raise NextY()

        except NextY:
            pass

    print(f"part 1: {best_y}")
    print(f"part 2: {len(velocities)}")


if __name__ == "__main__":
    solve()
