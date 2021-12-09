import collections
import math

from util import DelimitedLinesBlockInput


class Piece:
    def __init__(self, s):
        self.id = int(s[0][5:-1])
        self.picture = s[1:]

    def verticals(self):
        return ["".join(v) for v in zip(*self.picture)]

    def top(self):
        return self.picture[0]

    def bottom(self):
        return self.picture[-1]

    def left(self):
        return self.verticals()[0]

    def right(self):
        return self.verticals()[-1]

    def flip_h(self):
        self.picture = [row[::-1] for row in self.picture]

    def flip_v(self):
        self.picture = self.picture[::-1]

    def edges(self):
        v = self.verticals()
        return {self.picture[0], self.picture[-1], v[0], v[-1]}

    def rotate(self):
        self.picture = self.verticals()[::-1]

    def match_left(self, search):
        while True:
            if self.left() == search:
                self.set_image()
                return
            elif self.left() == search[::-1]:
                self.flip_v()
            else:
                self.rotate()

    def match_top(self, search):
        while True:
            if self.top() == search:
                self.set_image()
                return
            elif self.top() == search[::-1]:
                self.flip_h()
            else:
                self.rotate()

    def set_image(self):
        self.image = [line[1:-1] for line in self.picture[1:-1]]



def corner_ids(pieces):
    corner_ids = []
    for piece in pieces:
        other_edges = {edge for jig in pieces for edge in jig.edges() if piece.id != jig.id}
        edge_edges = 0
        for edge in piece.edges():
            if edge not in other_edges and edge[::-1] not in other_edges:
                edge_edges += 1
                if edge_edges == 2:
                    corner_ids.append(piece.id)
                    break
    return corner_ids


def part1():
    with DelimitedLinesBlockInput('./input.txt') as data:
        pieces = [Piece(d) for d in data]
        print(f"part 1: {math.prod(corner_ids(pieces))}")


def part2():
    with DelimitedLinesBlockInput('./input.txt') as data:
        pieces = [Piece(d) for d in data]
        corners = corner_ids(pieces)

        edge_lookup = collections.defaultdict(list)
        for piece in pieces:
            for edge in piece.edges():
                edge_lookup[edge].append(piece)

        # pick a corner and get it oriented
        a_corner_id = corners[0]
        a_corner = [p for p in pieces if p.id == a_corner_id][0]
        other_edges = {edge for jig in pieces for edge in jig.edges() if a_corner_id != jig.id}
        while True:
            if any(e in other_edges for e in {a_corner.top(), a_corner.top()[::-1], a_corner.left(), a_corner.left()[::-1]}):
                a_corner.rotate()
            else:
                break
        a_corner.set_image()

        arranged = []
        used = set()
        current_row = [a_corner]
        arranged.append(current_row)
        while True:
            used.add(current_row[-1].id)
            search = current_row[-1].right()
            match_p = [p for p in edge_lookup[search] + edge_lookup[search[::-1]] if p.id != current_row[-1].id and p.id not in used]
            if len(match_p) == 0:
                # next row
                vsearch = current_row[0].bottom()
                vmatch = [p for p in edge_lookup[vsearch] + edge_lookup[vsearch[::-1]] if p.id != current_row[0].id and p.id not in used]
                if len(vmatch) != 1:
                    if len(used) != len(pieces):
                        raise Exception(f"found {len(vmatch)} matches to start next row, used {len(used)}")
                    else:
                        break
                start_next_row = vmatch[0]
                start_next_row.match_top(vsearch)
                current_row = [start_next_row]
                arranged.append(current_row)
            elif len(match_p) == 1:
                next_piece = match_p[0]
                next_piece.match_left(search)
                current_row.append(next_piece)
            else:
                raise Exception(f"found {len(match_p)} matches :(")

        for tile_row in arranged:
            for i in range(len(tile_row[0].picture)):
                print(" ".join([tile.picture[i] for tile in tile_row]))
            print("")

        p = pieces[0]

        #print(" ".join(p.image[0] for p in arranged[0]))
        #print("")
        #print(list(map(lambda p: p.image, arranged[0])))
        #print(list(zip(map(lambda p: p.image, arranged[0]))))

        overall_pic = ["".join(z) for piece_row in arranged for z in zip(*map(lambda p: p.image, piece_row))]
        print("\n".join(overall_pic))

        sample = [
            "                  # ",
            "#    ##    ##    ###",
            " #  #  #  #  #  #   "
        ]
        pattern = [(y,x) for y, row in enumerate(sample) for x, c in enumerate(row) if c == '#']

        serpents = []
        print(list((dy, dx) for dy, dx in pattern))
        print(list((1 + dy, 1 + dx) for dy, dx in pattern))
        print(list((1 + dy, 2 + dx) for dy, dx in pattern))
        print(list(overall_pic[dy][dx] == '#' for dy, dx in pattern))
        for _ in range(2):
            for _ in range(4): # each rotation
                for y in range(len(overall_pic)-(len(sample)-1)):
                    for x in range(len(overall_pic[0])-(len(sample[0])-1)):
                        if all(overall_pic[y+dy][x+dx] == '#' for dy, dx in pattern):
                            serpents.append((y,x))
                if len(serpents) > 0:
                    break
                else:
                    overall_pic = ["".join(v) for v in zip(*overall_pic)][::-1]
                    print("\n".join(overall_pic))
            if len(serpents) > 0:
                break
            else:
                # flipping
                overall_pic = overall_pic[::-1]
        else:
            raise Exception("Where are all the monsters? :(")

        serpent_coords = {(y+dy,x+dx) for y,x in serpents for dy,dx in pattern}
        hash_coords = {(y,x) for y in range(len(overall_pic)) for x in range(len(overall_pic[0])) if overall_pic[y][x] == '#'}
        answer = len(hash_coords - serpent_coords)

        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()

