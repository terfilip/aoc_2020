
def to_int_list(s):
    return list(map(int, s))


def cups_after_1(s):
    if type(s) == list:
        s = ''.join(map(str,s))
    splt = s.split('1')
    return splt[1] + splt[0]


def pick_up_cups(cur_cup, lst):
    cci = lst.index(cur_cup)
    lstlen = len(lst)
    pickedup = []

    for i in range(1, 4):
        ii = cci + i
        if ii >= lstlen:
            ii -= lstlen
        pickedup.append(lst[ii])

    return pickedup


def select_dest_cup(cur_cup, picked_up, lst):
    dst = cur_cup - 1
    while dst in picked_up:
        dst -= 1

    if dst not in lst:
        dst = max(i for i in lst if i not in picked_up)
    return dst


def move_picked_up_cups(dest_cup, picked_up, lst):
    new_lst = [i for i in lst if i not in picked_up]
    destpos = new_lst.index(dest_cup)

    for i in range(1, 4):
        new_lst.insert(destpos + i, picked_up[i - 1])
    return new_lst


def sel_new_cur_cup(cur_cup, lst):
    curpos = lst.index(cur_cup)
    nextpos = curpos + 1

    if nextpos >= len(lst):
        nextpos -= len(lst)

    return lst[nextpos]


def move(cur_cup, lst):
    picked_up = pick_up_cups(cur_cup, lst)
    dest_cup = select_dest_cup(cur_cup, picked_up, lst)
    new_lst = move_picked_up_cups(dest_cup, picked_up, lst)
    new_cur_cup = sel_new_cur_cup(cur_cup, new_lst)
    return new_cur_cup, new_lst


def nmoves(n, lst):
    cur_cup = lst[0]

    for _ in range(n):
        cur_cup, lst = move(cur_cup, lst)
    return cur_cup, lst


def nmovesprint(n, lst):
    cur_cup = lst[0]

    for _ in range(n):
        cur_cup, lst = move(cur_cup, lst)
        s = ''
        for cup in lst:
            space = ' ' if cup < 10 else ''
            if cup != cur_cup:
                s += ' ' + space + str(cup) + ' '
            else:
                s += ' (' + space + str(cup) + ') '
        print(s)
    return cur_cup, lst


nums = to_int_list("123487596")
s1nums = to_int_list("389125467")

print('P1: ', cups_after_1(nmoves(100, nums)[1]))