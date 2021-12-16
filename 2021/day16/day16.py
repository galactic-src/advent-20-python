import math

from util import OneLineInput

bin_map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def parse_value(s):
    value_chars = ""
    keep_going = True
    while keep_going:
        next_chunk = s[0:5]
        s = s[5:]
        value_chars += next_chunk[1:]
        keep_going = next_chunk[0] == '1'

    return s, int(value_chars, 2)


def parse_all_packets(s, exact):
    packets = []
    while s:
        s, p = parse_packet(s)
        packets.append(p)
        if not exact and all(c == '0' for c in s):
            break
    return packets


def parse_n_packets(s, n):
    packets = []
    for _ in range(n):
        s, p = parse_packet(s)
        packets.append(p)
    return s, packets


def parse_packet(s):
    version = int(s[0:3], 2)
    ptype = int(s[3:6], 2)
    p = Packet(version, ptype)
    if ptype == 4:
        s, value = parse_value(s[6:])
        p.value = value
        return s, p
    elif s[6] == '0':
        len_str = s[7:7+15]
        subpacket_length = int(len_str, 2)
        subpacket_str = s[7+15:7+15+subpacket_length]
        subpackets = parse_all_packets(subpacket_str, True)
        p.subpackets.extend(subpackets)
        s = s[7+15+subpacket_length:]
    else:
        subpacket_count = int(s[7:7+11], 2)
        s, subpackets = parse_n_packets(s[7+11:], subpacket_count)
        p.subpackets = subpackets
    return s, p


class Packet:
    def __init__(self, version, ptype):
        self.version = version
        self.ptype = ptype
        self.value = None
        self.subpackets = []

    def versions_total(self):
        return sum(subpacket.versions_total() for subpacket in self.subpackets) + self.version

    def calc(self):
        if self.ptype == 0:
            return sum(p.calc() for p in self.subpackets)
        elif self.ptype == 1:
            return math.prod(p.calc() for p in self.subpackets)
        elif self.ptype == 2:
            return min(p.calc() for p in self.subpackets)
        elif self.ptype == 3:
            return max(p.calc() for p in self.subpackets)
        elif self.ptype == 4:
            return self.value
        elif self.ptype == 5:
            if len(self.subpackets) != 2:
                raise Exception("GT")
            return 1 if self.subpackets[0].calc() > self.subpackets[1].calc() else 0
        elif self.ptype == 6:
            if len(self.subpackets) != 2:
                raise Exception("LT")
            return 1 if self.subpackets[0].calc() < self.subpackets[1].calc() else 0
        elif self.ptype == 7:
            if len(self.subpackets) != 2:
                raise Exception("EQ")
            return 1 if self.subpackets[0].calc() == self.subpackets[1].calc() else 0
        else:
            raise Exception("ptype")


def to_bin(s):
    return "".join(bin_map[c] for c in s)


def part1():
    with OneLineInput('./input.txt') as data:
        packets = parse_all_packets(to_bin(data), False)

        answer = sum(packet.versions_total() for packet in packets)
        print(f"part 1: {answer}")


def part2():
    with OneLineInput('./input.txt') as data:
        answer = parse_all_packets(to_bin(data), False)[0].calc()
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
