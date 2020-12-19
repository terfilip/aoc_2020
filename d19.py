import itertools


def read_in(fname):

    with open(fname, "r") as f:

        rules = {}
        seqs = []

        while line := f.readline():
            line = line.strip()
            if line == "":
                break

            k, vs = line.split(": ")
            k = int(k)

            if '"' in vs:
                rules[k] = vs[1:-1]
            elif " | " in vs:
                vs = tuple(list(map(int, vss.split(" "))) for vss in vs.split(" | "))
                rules[k] = vs
            elif " " in vs:
                rules[k] = list(map(int, vs.split(" ")))
            else:
                rules[k] = int(vs)

        while line := f.readline():
            seqs.append(line.strip())

        return rules, seqs


rules, seqs = read_in("19.txt")
rulesv2, seqsv2 = read_in("19v2.txt")
s1rules, s1seqs = read_in("19sample1.txt")

def combine2_vals(la,lb):

    if la == str and lb == str:
        return la + lb

    if lb == str:
        lb = [lb]

    if la == str:
        la = [la]

    l = itertools.product(la, lb)
    return [''.join(i) for i in l]


def combine_vals(*vals):

    if all(type(x) == str for x in vals):
        return ''.join(vals)

    vls = [[x] if type(x) == str else x for x in vals]
    try:
        return [''.join(x) for x in itertools.product(*vls)]
    except TypeError:
        print(list(itertools.product(*vls)))
        print(vls)
        print(vals)
        raise


def find_rules_seq(inrules, rule):

    def _find_rules_seq(rule):
        ruleval = inrules[rule]

        if type(ruleval) == str:
            return ruleval

        if type(ruleval) == int:
            return _find_rules_seq(ruleval)

        if type(ruleval) == tuple:
            l1 = _find_rules_seq(ruleval[0][0])

            if len(ruleval[0]) > 1:
                l2 = _find_rules_seq(ruleval[0][1])
                l = combine_vals(l1, l2)
            else:
                l = l1
            r1 = _find_rules_seq(ruleval[1][0])

            if len(ruleval[1]) > 1:
                r2 = _find_rules_seq(ruleval[1][1])
                r = combine_vals(r1, r2)
            else:
                r = r1

            if type(l) == str:
                l = [l]

            if type(r) == str:
                r = [r]

            return l + r

        if type(ruleval) == list:
            found = [_find_rules_seq(x) for x in ruleval]
            return combine_vals(*found)

    return _find_rules_seq(rule)

#if False:
def p1():
    allowed_seqs1 = find_rules_seq(rules, 0)
    return len([seq for seq in seqs if seq in allowed_seqs1])

print('P1: ', p1())



