from util import ManyLineInput


class Food:
    def __init__(self, s):
        data = s.rstrip(')').split(' (contains ')
        self.ingredients = set(data[0].split(' '))
        if len(data) > 1:
            self.allergens = set(data[1].split(', '))


def get_candidate_map(data):
    allergen_candidates = {}
    for food in data:
        for a in food.allergens:
            if a in allergen_candidates:
                allergen_candidates[a] &= food.ingredients
            else:
                allergen_candidates[a] = set(food.ingredients)
    return allergen_candidates


def part1():
    with ManyLineInput('./input.txt', Food) as data:
        all_ingredients = {i for f in data for i in f.ingredients}
        allergen_candidates = get_candidate_map(data)

        maybe_dangerous = {i for l in allergen_candidates.values() for i in l}
        safe = all_ingredients - maybe_dangerous
        answer = sum(len(list(filter(lambda i: i in safe, f.ingredients))) for f in data)
        print(f"part 1: {answer}")


def part2():
    with ManyLineInput('./input.txt', Food) as data:
        candidates = get_candidate_map(data)
        identified = {}
        while candidates:
            for allergen, ingredients in candidates.items():
                possibles = [i for i in ingredients if i not in identified]
                if len(possibles) == 1:
                    found_a = allergen
                    found_i = possibles[0]
                    break

            candidates.pop(found_a)
            identified[found_i] = found_a

        answer = ','.join(i for i, _ in sorted(identified.items(), key=lambda m: m[1]))
        print(f"part 2: {answer}")


if __name__ == "__main__":
    part1()
    part2()
