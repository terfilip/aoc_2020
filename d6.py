answers = []


with open('6.txt', 'r') as f:

    chunk = []
    
    while line := f.readline():
        line = line.strip()

        if line != '':
            chunk.append(line)
        else:
            answers.append(chunk)
            chunk = []

    answers.append(chunk)


def n_all_ans(grp):
    
    ltop = {}

    for person, qans in enumerate(grp):
        
        for ltr in qans:
            try:
                ltop[ltr] = ltop[ltr].union({person})
            except KeyError:
                ltop[ltr] = {person}

    all_ans = {k: v for k, v in ltop.items() if v == set(range(len(grp)))}
    return len(all_ans)



print('P1: ', sum((len(set(''.join(grp_ans))) for grp_ans in answers)))
print('P2: ', sum((n_all_ans(grp_ans) for grp_ans in answers)))
