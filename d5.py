import numpy as np

instrs = []


with open('5.txt','r') as f:
    while line := f.readline():
        instrs.append(line.strip())


def find_val(instrs, uchar, dchar, lb, ub):

    ans = None
    
    for instr in instrs:
        if instr == uchar:
            lb = ub - (ub - lb) // 2
            ans = lb
        elif instr == dchar:
            ub = lb + (ub - lb) // 2
            ans = ub

    return ans

def find_seat(instrs):
    rowi = instrs[:7]
    coli = instrs[7:]

    assert len(coli) == 3

    rownum = find_val(rowi, 'B', 'F', 0, 127)
    colnum = find_val(coli, 'R', 'L', 0, 7)

    return rownum, colnum, rownum * 8 + colnum


seats = [find_seat(i) for i in instrs]
max_seat_id_seat = max(seats, key=lambda x: x[2])
print('P1: ', max_seat_id_seat[2])

seat_ids = sorted([s[2] for s in seats])

diffs = np.diff(seat_ids)
lb = np.where(diffs == 2)[0][0]
print('P2: ', seat_ids[lb] + 1)

