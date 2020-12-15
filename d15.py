from collections import defaultdict

def read_in(fname):
    with open(fname, 'r') as f:
        return list(map(int, f.readline().strip().split(',')))


start_nums = read_in('15.txt')


def run(start_nums, tgt):
    # num: [first_turn_where_spoken, second_turn_wh.....]
    num2turn = defaultdict(list)

    i = 1
    prev_num = None
    while i <= tgt:
        ii = i - 1

        if ii < len(start_nums):
            num2turn[start_nums[ii]].append(i)
            prev_num = start_nums[ii]
        else:
            n_occ = len(num2turn[prev_num])

            if n_occ < 2:
                num2turn[0].append(i)
                prev_num = 0
            else:
                k = num2turn[prev_num][-1] - num2turn[prev_num][-2]
                num2turn[k].append(i)
                prev_num = k

        i += 1

    return prev_num, num2turn


def p1():
    ans, _ = run(start_nums, 2020)
    print('P1: ', ans)


def p2():
    ans, _ = run(start_nums, int(3e7))
    print('P2: ', ans)

p1()
p2()

