from copy import copy

PRE_LEN = 25

with open('9.txt', 'r') as f:
    arr = [int(ln.strip()) for ln in f.readlines()]


def two_sum(nums, tgt):
    idx = {}

    for i, num in enumerate(nums):

        if tgt - num in idx.keys():
            j = idx[tgt - num]
            return j, i
        else:
            idx[num] = i
    raise ValueError("Answer not found")


def find_fst_invalid():
    i = PRE_LEN
    arr_len = len(arr)

    while i < arr_len:
        arr_slice = arr[i - PRE_LEN: i]

        try:
            ii, jj = two_sum(arr_slice, arr[i])
        except ValueError:
            return arr[i]
        i += 1
    raise ValueError("No invalid numbers")


def srs(nums, tgt):
    # sub range sum
    rng_sz = 4

    while rng_sz < len(nums):

        i = 0
        while i < len(nums):
            ss = nums[i: i + rng_sz]

            if sum(ss) == tgt:
                return ss
            i += 1
        rng_sz += 1

fst_invalid = find_fst_invalid()
print('P1: ', fst_invalid)

sum_range = srs(arr, fst_invalid)
print('P2: ', min(sum_range) + max(sum_range))

