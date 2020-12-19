import itertools
import re
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


def find_rules_seq(inrules, rule, rec_lim, target_seqs):
    call_ctr = {8: 0, 11: 0}
    memo = {}

    def _find_rules_seq(rule):
        ruleval = inrules[rule]

        if rule in [8, 11] and call_ctr[rule] < rec_lim:
            call_ctr[rule] += 1
        elif rule in [8,11] and call_ctr[rule] >= rec_lim:
            if rule == 8:
                return memo[42]
            elif rule == 11:
                base_case = "".join([memo[42], memo[31]])
                return base_case
        elif rule in memo.keys():
            return memo[rule]

        if type(ruleval) == str:
            ans = ruleval.strip()
        elif type(ruleval) == int:
            ans = _find_rules_seq(ruleval)
        elif type(ruleval) == tuple:
            l1 = _find_rules_seq(ruleval[0][0])

            if len(ruleval[0]) > 1:
                l2 = _find_rules_seq(ruleval[0][1])
                l = "".join([l1,l2])
            else:
                l = l1
            r1 = _find_rules_seq(ruleval[1][0])

            if len(ruleval[1]) > 1:
                r2 = _find_rules_seq(ruleval[1][1])

                if len(ruleval[1]) > 2:
                    r3 = _find_rules_seq(ruleval[1][2])
                    r = "".join([r1,r2,r3])
                else:
                    r = "".join([r1,r2])
            else:
                r = r1
            ans = f"({l}|{r})"
        elif type(ruleval) == list:
            found = [_find_rules_seq(x) for x in ruleval]
            ans = "".join(found)

        memo[rule] = ans
        return ans

    ptn = _find_rules_seq(rule)
    rgx = re.compile(ptn)
    cnt = len([s for s in target_seqs if rgx.fullmatch(s)])

    return cnt, rgx


print('P1: ', find_rules_seq(rules, 0, 1, seqs)[0])
print('P2: ', find_rules_seq(rulesv2, 0, 10, seqsv2)[0])

