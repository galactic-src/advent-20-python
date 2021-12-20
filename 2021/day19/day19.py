import collections
import numpy as np
from enum import Enum, auto
import re
from itertools import combinations, accumulate

from util import ManyLineInput, OneLineInput, windowed, DelimitedLinesBlockInput

# scanners see beacons in a cube centered on the scanner, <=1000units away along any axis
# find pairs of scanners that have overlapping regions and share 12 beacons
# scanner 0 defines 0,0,0 and coordinate system


def parse_coord(s):
    x, y, z = s.split(',')
    return int(x), int(y), int(z)


class Scanner:
    def __init__(self, block):
        self.id = int(block[0].lstrip('--- scanner ').rstrip(' ---'))
        self.beacons = [parse_coord(b) for b in block[1:]]
        self.beacon_distances = collections.defaultdict(list)
        for ix, beacon in enumerate(self.beacons):
            for ix2, beacon2 in enumerate(self.beacons):
                if ix < ix2:
                    self.beacon_distances[abs(beacon[0] - beacon2[0]) + abs(beacon[1] - beacon2[1]) + abs(beacon[2] - beacon2[2])].append((ix, ix2))
        print(self.beacon_distances)
        self.transform = np.identity(3) if self.id == 0 else None


def part1():
    # 12 beacon overlap would mean 12 + 11 + ... distances overlap
    required_overlap = 12 * (12+1) / 2
    print(f"need {required_overlap} overlap")

    with DelimitedLinesBlockInput('./example.txt') as data:
        scanners = [Scanner(block) for block in data]

        # line them up
        while any(s.transform is None for s in scanners):
            for scanner in scanners:
                for scanner2 in scanners:
                    if scanner.transform is not None and scanner2.transform is None:
                        common_distances = sum(min(len(pairs), len(scanner2.beacon_distances[distance])) for distance, pairs in scanner.beacon_distances.items())

                        if common_distances >= required_overlap:
                            for distance, ix_pairs1 in scanner.beacon_distances.items():
                                ix_pairs2 = scanner2.beacon_distances[distance]


                            # iterate over pairs of beacons with same distances between
                            # calculate vector between
                            # calculate rotation matrix to align scanners
                            # calculate translation matrix between scanners
                            # apply transform to all beacons
                            # check they now have 12+ identical beacons
                            # update scanner beacons and transform, or try next pair

        # set of all beacons from all scanners, now they are aligned
        # len

        answer = len({b for s in scanners for b in s.beacons})
        print(f"part 1: {answer}")


def part2():
    with DelimitedLinesBlockInput('./example.txt') as data:
        answer = ''
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()