import numpy as np
from copy import copy


def read_in(fname):
    with open(fname, 'r') as f:
        tile_ids = []
        tiles = []
        curarr = []

        while line := f.readline():
            line = line.strip()
            if line.startswith('Tile '):
                tile_id = int(line.split(' ')[1][:-1])
                tile_ids.append(tile_id)
            elif line == '':
                tiles.append(np.array(curarr))
                curarr = []
            else:
                curarr.append(list(line))
        tiles.append(np.array(curarr))
        return tile_ids, tiles


s1ids, s1tiles = read_in('20sample1.txt')
ids, tiles = read_in('20.txt')


def corner_id_prod(ids):
    return ids[0][0] * ids[0][-1] * ids[-1][0] * ids[-1][-1]


def aligned(arr1, arr2, is_vertical):
    if is_vertical:
        return (arr1[-1] == arr2[0]).all()
    else:
        return (arr1[:, -1] == arr2[:, 0]).all()


def all_aligned(tile_square):
    sqlen = len(tile_square)

    for i in range(sqlen - 1):
        for j in range(sqlen - 1):
            if ((not aligned(tile_square[i][j], tile_square[i + 1][j], is_vertical=True))
                    or (not aligned(tile_square[i][j], tile_square[i][j + 1], is_vertical=False))):
                return False

    return True


def iter_tiles(tiles):
    z = -1

    rotfun = lambda x: x if (k == 0 or x is None) else np.rot90(x, k=-k)
    flipfun = lambda x: x if (z == -1 or x is None) else np.flip(x, z)

    while z < 2:
        k = 0
        while k < 4:
            for i, tile in enumerate(tiles):
                yield i, flipfun(rotfun(tile))
            k += 1
        z += 1


def find_aligned_tile(tile, tiles, is_vertical):
    for i, ttile in iter_tiles(tiles):
        if ttile is None or (tile == ttile).all():
            continue

        if aligned(tile, ttile, is_vertical):
            return i, ttile

    raise ValueError('No matching tile found')


def create_aligned_square_with_start_tile(in_tiles, in_ids, istart_tile, start_tile):
    tiles = copy(in_tiles)
    ndim = int(np.sqrt(len(tiles)))
    square = np.full((ndim, ndim), None)
    id_square = np.full((ndim, ndim), None)

    square[0][0] = start_tile
    id_square[0][0] = in_ids[istart_tile]
    tiles[istart_tile] = None

    def fill_row_or_col(i, j, vertical):
        curtile = square[i][j]

        if vertical and i + 1 >= len(square):
            return
        elif not vertical and j + 1 >= len(square):
            return

        ialigned_tile, aligned_tile = find_aligned_tile(curtile, tiles, vertical)
        tiles[ialigned_tile] = None

        if vertical:
            square[i + 1][j] = aligned_tile
            id_square[i + 1][j] = in_ids[ialigned_tile]
            fill_row_or_col(i + 1, j, True)
        else:
            square[i][j + 1] = aligned_tile
            id_square[i][j + 1] = in_ids[ialigned_tile]
            fill_row_or_col(i, j + 1, False)

    for i in range(ndim):
        fill_row_or_col(i, 0, False)

        if i == 0:
            fill_row_or_col(0, 0, True)
    return square, id_square


def create_aligned_square(tiles, ids):
    for itile, tile in iter_tiles(tiles):
        try:
            sq, idsq = create_aligned_square_with_start_tile(tiles, ids, itile, tile)
            return sq, idsq
        except ValueError:
            pass


def merge_tiles(square):
    return np.concatenate([np.concatenate([tile[1:-1, 1:-1] for tile in tiles], axis=1) for tiles in square], axis=0)


def count_sea_monsters(tile, smp_arr):
    smp_rowlen, smp_collen = smp_arr.shape
    tile_rowlen, tile_collen = tile.shape
    monster_counter = 0

    for i in range(0, len(tile) - 3):
        for j in range(0, (tile_collen - smp_collen + 1)):
            cut = tile[i:i + 3, j:(20 + j)]
            smp_comp = np.where(smp_arr == ' ', cut, smp_arr)

            if (cut == smp_comp).all():
                monster_counter += 1

    return monster_counter


def count_remaining_hashes(monster_count, smp_arr, tile):
    smp_hash_count = np.where(smp_arr == '#')[0].size
    tile_hash_count = np.where(tile == '#')[0].size
    return tile_hash_count - (smp_hash_count * monster_count)


sq, idsq = create_aligned_square(tiles, ids)
print('P1: ', corner_id_prod(idsq))

sea_monster_pattern = '''                  # \n#    ##    ##    ###\n #  #  #  #  #  #   '''

smp_arr = np.array([list(smp) for smp in sea_monster_pattern.split('\n')])
merged_tile = merge_tiles(sq)

for itile, tile in iter_tiles([merged_tile]):
    monster_counter = count_sea_monsters(tile, smp_arr)
    if monster_counter != 0:
        break

print('P2: ', count_remaining_hashes(monster_counter, smp_arr, merged_tile))
