import re

from util import DelimitedLinesBlockInput

HEIGHT_REGEX = re.compile('^([0-9]+)(cm|in)$')
def valid_height(height):
    m = HEIGHT_REGEX.fullmatch(height)
    if m is None:
        return False

    try:
        n = int(m.group(1))
    except:
        return False

    if m.group(2) == 'cm':
        return 150 <= n <= 193
    elif m.group(2) == 'in':
        return 59 <= n <= 76
    else:
        return False


HCL_REG = re.compile('#[0-9a-f]{6}')
def valid_hcl(hcl):
    return HCL_REG.fullmatch(hcl) is not None


def valid_ecl(ecl):
    return ecl in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def year_between(yr, lo, hi):
    try:
        yr = int(yr)
        return lo <= yr <= hi
    except Exception:
        return False


PID_REG=re.compile('[0-9]{9}')
def valid_pid(pid):
    return PID_REG.fullmatch(pid) is not None


def fields_valid(passports):
    fields = {field[0]: field[1] for field in passports}
    return year_between(fields['byr'], 1920, 2002) \
        and year_between(fields['iyr'], 2010, 2020) \
        and year_between(fields['eyr'], 2020, 2030) \
        and valid_height(fields['hgt']) \
        and valid_hcl(fields['hcl']) \
        and valid_ecl(fields['ecl']) \
        and valid_pid(fields['pid'])


def keys_valid(passport):
    keys = {field[0] for field in passport}
    return keys.issuperset({'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'})


def passports(data):
    return map(lambda pgroup: [field.split(":") for line in pgroup for field in line.split(" ")], data)


def part1():
    with DelimitedLinesBlockInput('./input.txt') as data:
        answer = sum(map(keys_valid, passports(data)))
        print(f"part 1: {answer}")


def part2():
    with DelimitedLinesBlockInput('./input.txt') as data:
        answer = sum(map(lambda p: keys_valid(p) and fields_valid(p), passports(data)))
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

