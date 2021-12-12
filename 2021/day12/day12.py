from collections import defaultdict

from util import ManyLineInput


def findPaths(connections, path, visited, next, found_paths, can_revisit, revisited):
    new_path = list(path)
    new_visited = set(visited)
    new_path.append(next)

    if next.islower():
        new_visited.add(next)

    if next == "end":
        found_paths.append([step for step in new_path])
        return

    for step in connections[next]:
        if step not in new_visited:
            findPaths(connections, new_path, new_visited, step, found_paths, can_revisit, revisited)
        elif can_revisit and not revisited and step != "start":
            findPaths(connections, new_path, new_visited, step, found_paths, can_revisit, True)


def part1():
    with ManyLineInput('input.txt') as data:
        connections = defaultdict(list)
        for line in data:
            start, end = line.split("-")
            connections[start].append(end)
            connections[end].append(start)

        found_paths = []
        findPaths(connections, [], {}, "start", found_paths, False, False)

        print(f"part 1: {len(found_paths)}")


def part2():
    with ManyLineInput('input.txt') as data:
        connections = defaultdict(list)
        for line in data:
            start, end = line.split("-")
            connections[start].append(end)
            connections[end].append(start)

        found_paths = []
        findPaths(connections, [], {}, "start", found_paths, True, False)

        print(f"part 2: {len(found_paths)}")


if __name__ == "__main__":
    part1()
    part2()