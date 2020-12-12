import functools
import operator

grid = []

with open('3.txt', 'r') as f:
    
    while line := f.readline():
        grid.append(list(line.rstrip()))

grid_len = len(grid)
line_len = len(grid[0])

def find_trees(rshift, dshift):
    ii = jj = trees = 0
    while True:
        ii += dshift
        jj += rshift

        if jj >= line_len:
            jj = jj - line_len
        
        if ii >= grid_len:
            break

        if grid[ii][jj] == '#':
            trees += 1

    return trees

slope_configs = (
    (1,1),
    (3,1),
    (5,1),
    (7,1),
    (1,2)
)

print('P1: ', find_trees(3, 1))

slope_tree_counts = (find_trees(*cfg) for cfg in slope_configs)
tree_prod = functools.reduce(operator.mul, slope_tree_counts, 1)
print('P2: ', tree_prod)



