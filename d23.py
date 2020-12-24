from copy import copy

def to_int_list(s): return list(map(int, s))


class Node:

    def __init__(self, value: int, next: 'Node' = None):
        self.value = value
        self.next = next

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return self.__repr__()


class CircularLinkedList:

    def __init__(self, nums: list):
        self.head = Node(nums.pop())
        orig_head = self.head
        while True:
            try:
                i = nums.pop()
                self.add_first(Node(i))
            except IndexError:
                break
        orig_head.next = self.head

    def add_first(self, node):
        node.next = self.head
        self.head = node

    def remove_after(self, node, node_to_remove):
        node.next = node_to_remove.next

    def add_after(self, node, node_to_add):
        prev_nxt = node.next
        node.next = node_to_add
        node_to_add.next = prev_nxt

    def __repr__(self):
        cur = self.head
        s = f' {cur} '
        cur = cur.next

        while cur != self.head:
            s += f' {cur} '
            cur = cur.next
        return s


def cups_after_1(s):
    if type(s) == list:
        s = ''.join(map(str,s))
    splt = s.split('1')
    return splt[1] + splt[0]


def pick_up_cups(cur_cup_pos, lst):
    lstlen = len(lst)  # O(1)
    pickedup = []
    pickedup_indexes = []

    for i in range(1, 4):
        ii = cur_cup_pos + i
        if ii >= lstlen:
            ii -= lstlen
        pickedup.append(lst[ii])  # List get item is O(1)
        pickedup_indexes.append(ii)

    return pickedup, pickedup_indexes


def select_dest_cup(cur_cup, list_min, list_max, picked_up, largest4_in_lst):
    dst = cur_cup - 1
    while dst in picked_up:
        dst -= 1

    if not (list_min <= dst <= list_max):
        dst = max(i for i in largest4_in_lst if i not in picked_up)
    return dst


def swap(lst, i, j):
    lst[i], lst[j] = lst[j], lst[i]


def move_picked_up_cups(dest_cup, picked_up_indexes, lst):

    picked_up = [lst[picked_up_indexes[0]], lst[picked_up_indexes[1]], lst[picked_up_indexes[2]]]
    for i, p in enumerate(picked_up):
        lst.remove(p)

    destpos = lst.index(dest_cup)  # barf

    for i, p in enumerate(picked_up):
        lst.insert(destpos + i + 1, p)


def sel_new_cur_cup(cur_cup_pos, list_len):
    nextpos = cur_cup_pos + 1

    if nextpos >= list_len:
        nextpos -= list_len
    return nextpos


def move(cur_cup_pos, lst, lst_min, lst_max, largest4):
    picked_up, picked_up_indexes = pick_up_cups(cur_cup_pos, lst)
    dest_cup = select_dest_cup(lst[cur_cup_pos], lst_min, lst_max, picked_up, largest4)
    cur_cup = lst[cur_cup_pos]
    move_picked_up_cups(dest_cup, picked_up_indexes, lst)
    new_cur_cup_pos = sel_new_cur_cup(lst.index(cur_cup), len(lst))
    return new_cur_cup_pos


def nmoves(n, lst):
    cur_cup_pos = 0
    lst = copy(lst)
    largest4 = sorted(lst)[-4:]
    list_min, list_max = min(lst), max(lst)

    for i in range(n):
        cur_cup_pos = move(cur_cup_pos, lst, list_min, list_max, largest4)

        if i % 1000 == 0:
            print(f'{i} Moves done')

    return lst


def nmovesprint(n, lst):
    cur_cup = lst[0]
    cur_cup_pos = 0
    largest4 = sorted(lst)[-4:]
    list_min, list_max = min(lst), max(lst)
    lst = copy(lst)

    for _ in range(n):
        cur_cup_pos = move(cur_cup_pos, lst, list_min, list_max, largest4)
        print(cur_cup_pos)
        cur_cup = lst[cur_cup_pos]
        s = ''
        for cup in lst:
            space = ' ' if cup < 10 else ''
            if cup != cur_cup:
                s += ' ' + space + str(cup) + ' '
            else:
                s += ' (' + space + str(cup) + ') '
        print(s)
    return lst


nums = to_int_list("123487596")
s1nums = to_int_list("389125467")

print('P1: ', cups_after_1(nmoves(100, nums)))
numsp2 = nums + list(range(10, int(1e6) + 1))
