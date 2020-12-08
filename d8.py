import time
from copy import copy


def process_line(ln):
    splt = ln.split(' ')
    return splt[0], int(splt[1])


with open('8.txt', 'r') as f:
    instructions = [process_line(ln) for ln in f.readlines()]

executed_instructions = set()

def execute1():

    iptr = 0
    accumulator = 0

    while iptr < len(instructions):
        instr, value = instructions[iptr]

        if iptr in executed_instructions:
            return accumulator

        executed_instructions.add(iptr)

        if instr == 'nop':
            iptr += 1 
        elif instr == 'jmp':
            iptr += value
        elif instr == 'acc':
            accumulator += value
            iptr += 1
        else:
            raise ValueError('wtf')

def execute2(instructions):

    iptr = 0
    accumulator = 0
    executed_instructions = set()

    while iptr < len(instructions):
        instr, value = instructions[iptr]

        if iptr in executed_instructions:
            return None
        executed_instructions.add(iptr)

        if instr == 'nop':
            iptr += 1 
        elif instr == 'jmp':
            iptr += value
        elif instr == 'acc':
            accumulator += value
            iptr += 1
        else:
            raise ValueError('wtf')
    
    return accumulator


def gen_new_inst_all():
    

    for i in reversed(range(len(instructions))):

        if instructions[i][0] == 'acc':
            continue

        new = copy(instructions)

        if instructions[i][0] == 'jmp':
            new[i] = ('nop', instructions[i][1])
        elif instructions[i][0] == 'nop':
            new[i] = ('jmp', instructions[i][1])

        yield new


print('P1: ', execute1())

for new_instrs in gen_new_inst_all():

    res = execute2(new_instrs)

    if res is not None:
        print('P2: ', res)
        break

