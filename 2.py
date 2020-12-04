import re

RGX = r'(\d+)-(\d+) ([a-z]): ([a-z]+)$'
rgx = re.compile(RGX)


def is_valid_1(l, u, letter, strng):
    occ = strng.count(letter)
    return l <= occ <= u

def is_valid_2(i, j, letter, strng):
    x = strng[i - 1]
    y = strng[j - 1]
    return (x == letter) ^ (y == letter)


def process_line(line):
    match = rgx.match(line)
    gr = match.group
    components = (int(gr(1)), int(gr(2)), gr(3), gr(4))
    return components
 

with open('2.txt', 'r') as f:
    parsed = []

    while line := f.readline():
        line = line.rstrip()
        parsed.append(process_line(line))


print('P1: ', sum((int(is_valid_1(*ln)) for ln in parsed)))
print('P2: ', sum((int(is_valid_2(*ln)) for ln in parsed)))



