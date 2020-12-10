import numpy as np
import pandas as pd

def read_nums(fname):
    with open(fname, 'r') as f:
        return [int(l.strip()) for l in f.readlines()]

def make_joltages(nums):
    return [0] + sorted(nums) + [max(nums) + 3]

nums = read_nums('10.txt')
joltages = make_joltages(nums)
unique, counts = np.unique(np.diff(joltages), return_counts=True)


def calc_df(joltages):
    diffs = np.diff(joltages)
    prev = diffs[1]
    range_ids = [-1]
    rid = 1
    
    for i in diffs[1:]:

        if i == 1 and prev != 3:
            range_ids.append(rid)
        elif i == 3 or prev == 3:
            range_ids.append(-1)
            rid += 1
        else:
            raise ValueError('wtf')
        
        prev = i

    
    df = pd.DataFrame(dict(Jolts=joltages,
                           Diff=np.append(diffs, 0),
                           RangeId=np.append(range_ids, -1)))
    return df

#1 number can be arranged in 2 ways (in or out)
#2 numbers can be arranged in 4 ways 
#3 numbers can be arranged in 7 ways (can't take them all out to avoid breaking the chain)
get_tot = lambda df: df.RangeId.value_counts().drop(-1).map({1:2,2:4,3:7}).values.prod()

# Assuming uniques = [1,3] which it is for my input
print('P1: ', counts[0] * counts[1])
print('P2: ', get_tot(calc_df(joltages)))

print('     Sample data 1 result for P2: ', get_tot(calc_df(make_joltages(read_nums('10sample1.txt')))))
print('     Sample data 2 result for P2: ', get_tot(calc_df(make_joltages(read_nums('10sample2.txt')))))
