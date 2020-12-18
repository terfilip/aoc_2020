from operator import add, mul


def read_in(fname):
    with open(fname, 'r') as f:
        return [l.strip() for l in f.readlines()]


exps = read_in('18.txt')
exps_s1 = read_in('18sample1.txt')


class Node:

    opdict = {'+': add, '*': mul}

    def __init__(self, root, left, right):
        self.left = left
        self.right = right
        self.root = root

        try:
            self.root_val = self.opdict[root](left,right)
        except TypeError:
            print(left)
            print(right)
            raise

    def __repr__(self):
        s = f"Node(({self.root}), {self.left}, {self.right})"
        return s

    def __add__(self, other):
        oth = other.root_val if type(other) == Node else other
        return self.root_val + oth

    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        oth = other.root_val if type(other) == Node else other
        return self.root_val * oth


def split_parens(exp: str):
    def _split_parens(exp):

        items = []
        numchars = []

        for let in exp:
            if let == '(':
                result = _split_parens(exp)
                items.append(result)
            elif let == ')':
                if numchars:
                    items.append(int(''.join(numchars)))
                return items
            else:
                if let.isdigit():
                    numchars.append(let)
                else:
                    if numchars:
                        items.append(int(''.join(numchars)))
                        numchars = []

                    if let != ' ':
                        items.append(let)

        if numchars:
            items.append(int(''.join(numchars)))

        return items
    return _split_parens(iter(exp))


def evaluate(parsed) -> int:

    if type(parsed[0]) == int:
        res = parsed[0]
    elif type(parsed[0]) == list:
        res = evaluate(parsed[0])
    else:
        raise ValueError('wtf')

    cur_op = None
    for item in parsed[1:]:

        if type(item) == str:
            cur_op = {'+': add, '*': mul}[item]
        elif type(item) == int:
            res = cur_op(res, item)
        elif type(item) == list:
            res = cur_op(res, evaluate(item))
        else:
            raise ValueError('wtf2')

    return res


def evaluate_line(line):
    return evaluate(split_parens(line))


def conv_to_node(items, op, other_op):

    i = 1

    if type(items) == Node:
        return items
    elif type(items[0]) == list:
        new_items = [conv_to_node(items[0], op, other_op)]
    else:
        new_items = [items[0]]

    while i < (len(items) - 1):
        item = items[i]
        nextitem = items[i + 1]
        if type(nextitem) == list:
            nextitem = conv_to_node(nextitem, op, other_op)

        if op == item:
            last = new_items.pop()
            if type(nextitem) == list:
                nextitem = conv_to_node(nextitem, other_op, op)
            if type(last) == list:
                last = conv_to_node(last, other_op, op)

            new_items.append(Node(op, last, nextitem))
        elif other_op == item:
            last = new_items.pop()
            new_items.extend([last, items[i], nextitem])

        i += 2

    if len(new_items) == 1 and type(new_items[0]) == Node:
        return new_items[0]
    else:
        return new_items


print('P1: ', sum(evaluate_line(line) for line in exps))


def evaluate_line2(line):
    sp = split_parens(line)
    node = conv_to_node(conv_to_node(sp, '+', '*'), '*', '+')
    return node.root_val

print('P2: ', sum(evaluate_line2(line) for line in exps))
