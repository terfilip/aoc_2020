from copy import copy
from typing import Union


def to_int_list(s): return list(map(int, s))


class Node:

    def __init__(self, value: int, next: 'Node'=None, node_m1=None):
        self.value = value
        self.next = next
        self.node_m1 = node_m1

    def __eq__(self, other):
        if type(other) == Node:
            return self.value == other.value
        elif type(other) == int:
            return self.value == other
        elif other is None:
            return False
        else:
            print(type(other))
            raise NotImplementedError('wtf')

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return self.__repr__()

    def __lt__(self, other):
        if type(other) == Node:
            return self.value < other.value
        elif type(other) == int:
            return self.value < other
        else:
            print(type(other))
            raise NotImplementedError('wtf')

    def __gt__(self, other):
        if type(other) == Node:
            return self.value > other.value


class CircularLinkedList:

    def __init__(self, nums: list):
        max4 = sorted(nums)[-4:]
        self.largest4 = []

        self.head = Node(nums.pop())
        orig_head = self.head
        nodelist = [orig_head]

        if orig_head.value in max4:
            self.largest4.append(orig_head)

        while True:
            try:
                n = nums.pop()
                node = Node(n)
                self.add_first(node)
                if n in max4:
                    self.largest4.append(node)
                nodelist.append(node)
            except IndexError:
                break
        nodelist.sort()

        for i in reversed(range(1, len(nodelist))):
            nodelist[i].node_m1 = nodelist[i - 1]
        nodelist[0].node_m1 = None

        orig_head.next = self.head

    def add_first(self, node):
        node.next = self.head
        self.head = node

    def remove_after(self, node):
        node_to_remove = node.next
        node.next = node_to_remove.next
        return node_to_remove

    def add_after(self, node, node_to_add):
        prev_nxt = node.next
        node.next = node_to_add
        node_to_add.next = prev_nxt

    def find(self, val: Union[int, Node], start_node=None):

        if start_node is None or self.head == start_node:
            orig = cur = self.head

            if cur == val:
                return cur
            cur = cur.next
        else:
            orig = cur = start_node

            if cur == val:
                return cur
            cur = cur.next

        while cur != orig:
            if cur == val:
                return cur
            cur = cur.next

        return None

    def __repr__(self):
        cur = self.head
        s = f' {cur} '
        cur = cur.next

        while cur != self.head:
            s += f' {cur} '
            cur = cur.next
        return s

    def print_first_n(self, n):
        cur = self.head
        s = f' {cur} '
        cur = cur.next
        i = 0

        while cur != self.head and i < n:
            s += f' {cur} '
            cur = cur.next
            i += 1


def cups_after_1(s):
    if type(s) == list:
        s = ''.join(map(str, s))
    splt = s.split('1')
    return splt[1] + splt[0]


def pick_up_cups(cur_cup, cll):
    pickedup = []

    for _ in range(3):
        pickedup.append(cll.remove_after(cur_cup))
    return pickedup


def select_dest_cup(cur_cup, picked_up, cll):
    dst = cur_cup.node_m1

    if dst is not None:
        while dst in picked_up:
            dst = dst.node_m1

    if dst is None:
        dst = max(i for i in cll.largest4 if i not in picked_up)
    return dst


def move_picked_up_cups(dest_cup, picked_up, cll):

    for p in reversed(picked_up):
        cll.add_after(dest_cup, p)


def sel_new_cur_cup(cur_cup_pos, list_len):
    nextpos = cur_cup_pos + 1

    if nextpos >= list_len:
        nextpos -= list_len
    return nextpos


def move(cll, cur_cup):
    picked_up = pick_up_cups(cur_cup, cll)
    dest_cup = select_dest_cup(cur_cup, picked_up, cll)
    move_picked_up_cups(dest_cup, picked_up, cll)
    new_cur_cup = cur_cup.next
    return new_cur_cup


def nmoves(n, lst):
    cll = CircularLinkedList(copy(lst))
    cur_cup = cll.head

    for i in range(n):
        cur_cup = move(cll, cur_cup)

        if i % 1000 == 0:
            print(f'{i} Moves done ', end='\r')

    return cll


def nmovesprint(n, lst):
    cll = CircularLinkedList(copy(lst))
    cur_cup = cll.head
    print('Cur cup: ', cur_cup)
    print(cll)
    print(cll.largest4)
    print()

    for _ in range(n):
        cur_cup = move(cll, cur_cup)
        print('Cur cup: ', cur_cup)
        print(cll)
        print()
    return cll


nums = to_int_list("123487596")
s1nums = to_int_list("389125467")

cll = nmoves(100, nums)
one = cll.find(1)
postones = []
nxt = one.next

while nxt != one:
    postones.append(nxt.value)
    nxt = nxt.next

print('P1: ', ''.join(map(str, postones)))
numsp2 = nums + list(range(10, int(1e6) + 1))
s1numsp2 = s1nums + list(range(10, int(1e6) + 1))

cll = nmoves(int(1e7), numsp2)
node_one = cll.find(1)
print()
print('P1: ', node_one.next.value * node_one.next.next.value)