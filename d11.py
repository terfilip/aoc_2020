from copy import deepcopy


def read_grid(fname):
    with open(fname, 'r') as f:
        return [list(l.strip()) for l in f.readlines()]

grid = read_grid('11.txt')
grid_sample_1 = read_grid('11sample1.txt')
grid_sample_2 = read_grid('11sample2.txt')
grid_sample_3 = read_grid('11sample3.txt')
grid_sample_4 = read_grid('11sample4.txt')

def get_adjacent_seat(grid, i, j):
    if i < 0 or j < 0:
        return None

    try:
        return grid[i][j]
    except IndexError:
        return None

def get_adjacent_seats(grid, i, j):
    coords = (
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1)
    )
    seats = (get_adjacent_seat(grid, *coord) for coord in coords)
    return (seat for seat in seats if seat is not None)

def count_occupied_seats(grid):
    if type(grid[0]) == list:
        return len([s for row in grid for s in row if s == '#'])
    else:
        return len([s for s in grid if s == '#'])

def show_grid(grid):
    print('\n'.join([''.join(row) for row in grid]))


def find_seat_in_direction(grid, i, j, move_in_direction):
    i, j = move_in_direction(i, j)
    adj_seat = get_adjacent_seat(grid, i, j)

    while adj_seat == '.':
        i, j = move_in_direction(i, j)
        adj_seat = get_adjacent_seat(grid, i, j)
    return adj_seat


def get_visible_seats(grid, i, j):
    seats = [
        find_seat_in_direction(grid, i, j, (lambda i, j: (i, j - 1))), # Left
        find_seat_in_direction(grid, i, j, (lambda i, j: (i - 1, j - 1))), # Top Left
        find_seat_in_direction(grid, i, j, (lambda i, j: (i + 1, j - 1))), # Bottom Left
        find_seat_in_direction(grid, i, j, (lambda i, j: (i + 1, j))), # Bottom
        find_seat_in_direction(grid, i, j, (lambda i, j: (i - 1, j))), # Top
        find_seat_in_direction(grid, i, j, (lambda i, j: (i, j + 1))), # Right
        find_seat_in_direction(grid, i, j, (lambda i, j: (i + 1, j + 1))), # Top Right
        find_seat_in_direction(grid, i, j, (lambda i, j: (i - 1, j + 1))), # Bottom Left
    ]
    return (seat for seat in seats if seat is not None)


def fill(grid, adj_seat_fn, n_occ_thresh):
    grid_prev = deepcopy(grid)
    grid_now = deepcopy(grid)

    while True:
        
        for i, row in enumerate(grid_prev):
            for j, val in enumerate(row):

                if val == '.':
                    continue
                n_adj_occ_seats = count_occupied_seats(list(adj_seat_fn(grid_prev, i, j)))

                if val == 'L' and n_adj_occ_seats == 0:
                    grid_now[i][j] = '#'
                elif val == '#' and n_adj_occ_seats >= n_occ_thresh:
                    grid_now[i][j] = 'L'
        if grid_now == grid_prev:
            return grid_now

        grid_prev = deepcopy(grid_now)
    return None

print('P1: ', count_occupied_seats(fill(grid, get_adjacent_seats, 4)))
print('P2: ', count_occupied_seats(fill(grid, get_visible_seats, 5)))

    
