from collections import defaultdict

from util import ManyLineInput


class Caves:
    def __init__(self, lines, can_revisit_small):
        self.connections = defaultdict(list)
        for line in lines:
            start, end = line.split("-")
            self.connections[start].append(end)
            self.connections[end].append(start)
        self.can_revisit_small = can_revisit_small

    def find_all_paths(self):
        found_paths = []
        self.find_paths([], {}, "start", found_paths, False)
        return found_paths

    def find_paths(self, path, visited, next, found_paths, revisited):
        new_path = list(path)
        new_visited = set(visited)
        new_path.append(next)

        if next.islower():
            new_visited.add(next)

        if next == "end":
            found_paths.append([step for step in new_path])
            return

        for step in self.connections[next]:
            if step not in new_visited:
                self.find_paths(new_path, new_visited, step, found_paths, revisited)
            elif self.can_revisit_small and not revisited and step != "start":
                self.find_paths(new_path, new_visited, step, found_paths, True)


def part1():
    with ManyLineInput('input.txt') as data:
        caves = Caves(data, False)
        paths = caves.find_all_paths()

        print(f"part 1: {len(paths)}")


def part2():
    with ManyLineInput('input.txt') as data:
        caves = Caves(data, True)
        paths = caves.find_all_paths()

        print(f"part 2: {len(paths)}")


if __name__ == "__main__":
    part1()
    part2()
