from collections import defaultdict


def process_dirs(line):
    i = 0
    dirs = []

    while i < len(line):
        nxt = line[i:i+2]
        if nxt[0] in 'ew':
            dirs.append(nxt[0])
            i += 1
        else:
            dirs.append(nxt)
            i += 2
    return dirs


def read_in(fname):

    with open(fname, 'r') as f:
        return [process_dirs(line.strip()) for line in f.readlines()]


dir2move = dict(
    nw=lambda x, y, z: (x + 1, y - 1, z),
    ne=lambda x, y, z: (x, y - 1, z + 1),
    e=lambda x, y, z: (x - 1, y, z + 1),
    se=lambda x, y, z: (x - 1, y + 1, z),
    sw=lambda x, y, z: (x, y + 1, z - 1),
    w=lambda x, y, z: (x + 1, y, z - 1)
)


def move_in_direction(dir, pos):
    return dir2move[dir](*pos)


def find_tile(dirs):
    pos = (0, 0, 0)

    for dir in dirs:
        pos = move_in_direction(dir, pos)
    return pos


def make_tile_dict(instructions):
    tiledict = defaultdict(int)

    for dirs in instructions:
        coords = find_tile(dirs)
        tiledict[coords] += 1
    return tiledict


def count_black_tiles(tiledict):
    return len([v for k,v in tiledict.items() if v % 2 != 0])


def one_round(tiledict):
    tiles_to_flip = []
    tiles_to_add = []

    for _ in range(2):
        for tile in tiledict.keys():
            neighbours = [move_in_direction(*tile) for move_in_direction in dir2move.values()]
            for neigh in neighbours:
                if neigh not in tiledict.keys():
                    tiles_to_add.append(neigh)

        for tta in tiles_to_add:
            tiledict[tta] = 0

    for tile, flipcnt in tiledict.items():
        neighbours = [move_in_direction(*tile) for move_in_direction in dir2move.values()]
        vls = [tiledict.get(neigh, 0) for neigh in neighbours]
        nblack = len([v for v in vls if v % 2 != 0])

        if flipcnt % 2 == 0: # tile itself if white
            if nblack == 2:
                tiles_to_flip.append(tile)
        else: # tile itself is black
            if nblack == 0 or nblack > 2:
                tiles_to_flip.append(tile)

    for ttf in tiles_to_flip:
        tiledict[ttf] += 1
    return tiledict


def runp2(tiles):
    td = make_tile_dict(tiles)

    for i in range(1, 101):
        td = one_round(td)
        print(f'P2 Day {i}: {count_black_tiles(td)}', end='\r')
    print()


tiles = read_in('24.txt')
s1tiles = read_in('24sample1.txt')

print('P1: ', count_black_tiles(make_tile_dict(tiles)))
runp2(tiles) #Day 100 is the answer to p2
