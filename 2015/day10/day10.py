def next_string(input):
    output = ''
    current = None
    count = 0
    for c in input:
        if c == current:
            count += 1
        else:
            if current:
                output += str(count)
                output += current
            current = c
            count = 1
    output += str(count)
    output += current
    return output


def part1():
    s = '1113122113'
    for _ in range(40):
        s = next_string(s)
    print(f"part 1: {len(s)}")


def part2():
    s = '1113122113'
    for _ in range(50):
        s = next_string(s)
    print(f"part 2: {len(s)}")


if __name__ == "__main__":
    part1()
    part2()

