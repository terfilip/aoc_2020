
            def read_instr(fname):
    with open(fname, 'r') as f:
        return [(i[0], int(i[1:])) for i in f.readlines()]


def move_in_dir(curx, cury, dir, n):
    dir_to_deg = dict(N=0, E=90, S=180, W=270)
    move_in_dir_dct = {
        0: lambda x, y: (x, y + n),
        90: lambda x, y: (x + n, y),
        180: lambda x, y: (x, y - n),
        270: lambda x, y: (x - n, y)
    }

    if type(dir) == str:
        dir = dir_to_deg[dir]

    return move_in_dir_dct[dir](curx, cury)


def rotate(cur_rot, leftright, ndeg):

    if leftright == 'R':
        new_rot = cur_rot + ndeg

        if new_rot >= 360:
            new_rot -= 360
    elif leftright == 'L':
        new_rot = cur_rot - ndeg

        if new_rot < 0:
            new_rot += 360
    else:
        raise ValueError('wtf')

    return new_rot


def rotate_waypoint(wpx, wpy, leftright, ndeg):

    ntimes = ndeg // 90
    assert leftright in 'LR'
    rotate = (lambda x, y: (y, -x)) if leftright == 'R' else (lambda x, y: (-y, x))

    for _ in range(ntimes):
        wpx, wpy = rotate(wpx, wpy)

    return wpx, wpy


def move_ship_to_waypoint(curx, cury, wx, wy, ntimes):
    return curx + wx * ntimes, cury + wy * ntimes


def follow(instructions):
    cur_rot = 90
    curx = 0
    cury = 0

    for inst, val in instructions:

        if inst == 'F':
            curx, cury = move_in_dir(curx, cury, cur_rot, val)
        elif inst in 'NSEW':
            curx, cury = move_in_dir(curx, cury, inst, val)
        elif inst in 'LR':
            cur_rot = rotate(cur_rot, inst, val)
    return curx, cury


def follow2(instructions):
    curx = 0
    cury = 0
    wx = 10
    wy = 1

    for inst, val in instructions:

        if inst == 'F':
            curx, cury = move_ship_to_waypoint(curx, cury, wx, wy, val)
        elif inst in 'NSEW':
            wx, wy = move_in_dir(wx, wy, inst, val)
        elif inst in 'LR':
            wx, wy = rotate_waypoint(wx, wy, inst, val)
    return curx, cury


def res(ffn):
    resx, resy = ffn(instructions)
    return abs(resx) + abs(resy)


instructions = read_instr('12.txt')
instr_sample_1 = read_instr('12sample1.txt')
print('P1: ', res(follow))
print('P2: ', res(follow2))
