from collections import OrderedDict
from functools import reduce

import numpy as np
import pandas as pd


def read_in(fname):
    with open(fname, 'r') as f:
        ts = int(f.readline())
        entries = [int(i) if i != 'x' else i for i in f.readline().split(',')]
        bus_ids = [i for i in entries if i != 'x']

        return ts, bus_ids, entries


ts, bus_ids, entries = read_in('13.txt')
sts, sbids, sentries = read_in('13sample1.txt') # sts stands for sample time stamp and so on
bus_dep_diffs = [entries.index(bid) for bid in bus_ids]


def find_earliest_bus_departures(sts, sbids):
    
    earliest_bus_timestamps = [sts - (sts % i) + i for i in sbids]
    earliest_bus_timestamp = min(earliest_bus_timestamps)
    earliest_bus_id = sbids[earliest_bus_timestamps.index(earliest_bus_timestamp)]
    return earliest_bus_timestamp, earliest_bus_id


def create_bus_diagram(start, end, bus_ids):

    rng = np.array(range(start, end))
    df = pd.DataFrame(index=rng)

    for bid in bus_ids:
        df[bid] = np.where(rng % bid == 0, 'D', '.')

    return df


def entries_to_ts_diff(entries):
    d = OrderedDict()
    for i, e in enumerate(entries):
        if i == 0:
            d[e] = e
        elif e != 'x':
            d[e] = i

    return d


def chinese_remainder(n, a):
    # CRT implementation from: https://rosettacode.org/wiki/Chinese_remainder_theorem#Python
    summ = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        summ += a_i * mul_inv(p, n_i) * p
    return summ % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1


def p1():
    ets, bus_id = find_earliest_bus_departures(ts, bus_ids)
    ans = bus_id * (ets - ts)
    print('P1: ', ans)


def p2():
    """
    A system of linear congruence equations
    ts = a_i modulo n_i
    ts =  ...
    ts =  ...

    where a_i = bus_id_i - diff_from_start_ts_i
            n_i = bus_id_i

    Can be solved with the Chinese Remainder Theorem
    """

    etdr = entries_to_ts_diff(entries)
    N = list(etdr.keys())
    A = [k - v for k, v in etdr.items()]
    ans = chinese_remainder(N, A)
    print('P2: ', ans)

p1()
p2()
