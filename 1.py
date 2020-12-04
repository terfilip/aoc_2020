
with open('1.txt', 'r') as f:
    nums = list(map(int, f.readlines()))

def two_sum(nums, tgt):

    idx = {}

    for i, num in enumerate(nums):

        if tgt - num in idx.keys():
            j = idx[tgt - num]
            return j, i
        else:
            idx[num] = i
    
    raise ValueError("Answer not found")


i, j = two_sum(nums, 2020)
x, y = nums[i], nums[j]
print('P1: ', x * y)

def three_sum(nums, tgt):

    idx = {}


    for i, inum in enumerate(nums):
        cur_tgt = tgt - inum
        for j, jnum in enumerate(nums):

            if cur_tgt - jnum in idx.keys():
                k = idx[cur_tgt - jnum]
                return i, j, k
            else:
                idx[jnum] = j
    
    raise ValueError("Answer not found")

i, j, k = three_sum(nums, 2020)
x, y, z = nums[i], nums[j], nums[k]
print('P2: ', x * y * z)