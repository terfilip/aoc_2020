import itertools
from copy import deepcopy

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
s2rules, s2seqs = read_in("19sample2.txt")


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


def find_rules_seq(inrules, rule, rec_lim, target_seqs):
    call_ctr = {8: 0, 11: 0}
    inrules = deepcopy(inrules)
    memo = {}
    #inrules[8] = ([42], [42, ([42], [42])])bbbbb
    #inrules[11] = ([42, 31], [42, ([42, 31], [42, 31]), 31])
    #init_loop_rule = {8: ([42], [42]),
    #                  11: ([42, 31], [42, 31])}
    MAX_WRITES = 4

    def _find_rules_seq(rule):
        ruleval = inrules[rule]
        #print('Rule: ', rule)

        if rule in memo.keys():
            return memo[rule]

        if rule in [8, 11] and call_ctr[rule] < rec_lim:
            #print(call_ctr)
            call_ctr[rule] += 1
        elif rule in [8,11] and call_ctr[rule] >= rec_lim:
            if rule == 8:
                print('rule 8 limit')
                inrules[8] = 42
                ans = memo[42]
                memo[8] = ans
                #ans = [s2 for s2 in ans if any(s2 in target_seq for target_seq in target_seqs)]
                #print(ans)
                return ans
            elif rule == 11:
                print('rule 11 limit')
                inrules[11] = [42, 31]
                found = [memo[42], memo[31]]
                ans = combine_vals(*found)
                memo[11] = ans
                #ans = [s2 for s2 in ans if any(s2 in target_seq for target_seq in target_seqs)]
                #print(ans)
                #print('herrow')
                return ans

        if type(ruleval) == str:
            ans = ruleval.strip()
        elif type(ruleval) == int:
            ans = _find_rules_seq(ruleval)
        elif type(ruleval) == tuple:
            l1 = _find_rules_seq(ruleval[0][0])

            if len(ruleval[0]) > 1:
                l2 = _find_rules_seq(ruleval[0][1])
                l = combine_vals(l1, l2)
            else:
                l = l1
            r1 = _find_rules_seq(ruleval[1][0])

            if len(ruleval[1]) > 1:
                r2 = _find_rules_seq(ruleval[1][1])

                if len(ruleval[1]) > 2: # Part 2 rule 11 only
                    r3 = _find_rules_seq(ruleval[1][2])
                    r = combine_vals(r1, r2, r3)
                else:
                    r = combine_vals(r1, r2)
            else:
                r = r1

            if type(l) == str:
                l = [l]

            if type(r) == str:
                r = [r]

            ans = l + r
        elif type(ruleval) == list:
            found = [_find_rules_seq(x) for x in ruleval]
            ans = combine_vals(*found)

        # If the generated strings are not substrings of any of the target sequences,
        # then the strings they produce will not be any of the target sequences so they can be discarded
        ans = [s2 for s2 in ans if any(s2 in target_seq for target_seq in target_seqs)]
        memo[rule] = ans
        return ans

    return _find_rules_seq(rule)


def get_ans(rules, seqs, reclim):
    ans = find_rules_seq(rules, 0, reclim, seqs)
    valid_seqs = [s for s in seqs if s in ans]
    return len(valid_seqs), valid_seqs

if False:
    def p1():
        allowed_seqs1 = find_rules_seq(rules, 0)
        return len([seq for seq in seqs if seq in allowed_seqs1])

    print('P1: ', p1())



