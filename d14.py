import itertools


class MaskedArray:

    def __init__(self, curmask=None, version=1):
        self.mem = {}

        if curmask is not None:
            self._current_mask = curmask
        self.version = version

    @property
    def current_mask(self):
        return self._current_mask

    @current_mask.setter
    def current_mask(self, curmask):
        self._current_mask = curmask

    def __getitem__(self, i):
        return self.mem[i]

    def __setitem__(self, k, v):

        if self.version == 1:
            self.mem[k] = apply_mask(v, self._current_mask)
        elif self.version == 2:
            addresses = apply_mask2(k, self._current_mask)

            for addr in addresses:
                self.mem[addr] = v

    def sum_mem(self):
        return sum(self.mem.values())


def apply_mask(number, mask):
    apply_bit_mask = lambda m, x: m if m != 'X' else x
    bin36num = format(number, 'b').zfill(36)
    return int(''.join(apply_bit_mask(m, x) for m, x in zip(mask, bin36num)), 2)


def apply_mask2(number, mask):
    apply_bit_mask = lambda m, x: m if m != '0' else x
    bin36num = format(number, 'b').zfill(36)
    masked_bits = [apply_bit_mask(m, x) for m, x in zip(mask, bin36num)]
    xcount = len([b for b in masked_bits if b == 'X'])

    if not xcount:
        return [int(''.join(masked_bits), 2)]
    possible_nums = []

    for possible_bits in itertools.product([0,1], repeat=xcount):
        possible_num = ''.join(masked_bits)
        for bit in possible_bits:
            possible_num = possible_num.replace('X', str(bit), 1)

        possible_nums.append(int(possible_num, 2))
    return possible_nums


def extract(l):
    pair = l.strip().split(' = ')

    if 'mem' in pair[0]:
        mem_idx = int(pair[0][:-1].replace('mem[',''))
        pair[1] = int(pair[1])
        pair.append(mem_idx)
    return pair


def read_inprog(fname):
    with open(fname,'r') as f:
        instrs = [extract(l) for l in f.readlines()]
        return instrs


inprog = read_inprog('14.txt')
inprog_s1 = read_inprog('14sample1.txt')


def run_inprog(inprog, masked_array_version):
    masked_array = MaskedArray(version=masked_array_version)

    for instruction in inprog:
        if instruction[0] == 'mask':
            masked_array.current_mask = instruction[1]
        else:
            _, number, index = instruction
            masked_array[index] = number

    return masked_array.sum_mem()


print('P1: ', run_inprog(inprog, 1))
print('P2: ', run_inprog(inprog, 2))