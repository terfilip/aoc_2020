from collections import Counter
import pandas as pd


def process_line(line):
    ings, allr = line.strip().split(' (contains ')
    allr = allr[:-1]
    return ings.split(' '), allr.split(', ')


def find_ans(inrules):
    all_allergens_uniq = {item for sublist in [item[1] for item in inrules] for item in sublist}
    all_ingredients = [item for sublist in [item[0] for item in inrules] for item in sublist]
    all_ingredients_uniq = set(all_ingredients)
    grid = pd.DataFrame(index=list(all_ingredients_uniq), columns=list(all_allergens_uniq), data=0)

    for rule in inrules:
        for allergen in rule[1]:
            for ingredient in rule[0]:
                grid.at[ingredient, allergen] += 1
    maxes = grid.max()
    nonall = grid.apply(lambda row: (row < maxes).all(), axis=1)
    nonall = nonall[nonall]
    ingredient_ctr = Counter(all_ingredients)
    sm = 0

    for i, na in nonall.items():
        sm += ingredient_ctr[i]
    return sm, grid, nonall


def make_cdil(grid):
    maxes = grid.max()
    cdil = []  # Canonical Dangerous Ingredient List

    while len(grid):
        idxs_to_drop = []
        for col in grid:
            argmaxes = grid[col] == maxes[col]
            argmaxes = argmaxes[argmaxes]

            if len(argmaxes) == 1:
                cdil.append((argmaxes.index[0], col))
                idxs_to_drop.append(argmaxes.index[0])
        grid = grid.drop(idxs_to_drop)
    return cdil


def format_cdil(cdil):
    cdil = sorted(cdil, key=lambda x: x[1])
    return ','.join(x[0] for x in cdil)


def read_in(fname):
    with open(fname, 'r') as f:
        return [process_line(line) for line in f.readlines()]


inrules = read_in('21.txt')
s1_inrules = read_in('21sample1.txt')
sm, grid, nonall = find_ans(inrules)
sms1, grids1, nonalls1 = find_ans(s1_inrules)
print('P1: ', sm)
aller_g = grid.drop(nonall.index)
cdil = make_cdil(aller_g)
print(f'P2: "{format_cdil(cdil)}"')
