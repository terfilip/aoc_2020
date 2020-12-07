import re


def process_line(line):
    cline = line.rstrip('. \n')

    if len(cline) != (len(line) - 2) and len(cline) != (len(line) - 1):
        print(cline)
        print(line)
        print(len(line) - len(cline))
        raise ValueError('wtf')

    comp1 = cline.replace('bags', 'bag').split(' contain ')
    comp2 = comp1[1].split(', ')

    if comp2[0] == 'no other bag':
        val = ()
    else:
        val = tuple([(int(s[0]), s[2:]) for s in comp2])

    return comp1[0], val


def find_bags_leading_to_shiny_gold(input_node):

    visited = set()
    leads_to_shiny_gold = set()

    def dfs(node, pnode):
        if node not in visited:
            visited.add(node)
            res = False

            for neigh in bag_graph[node]:

                if neigh[1] == 'shiny gold bag':
                    leads_to_shiny_gold.add(node)
                    if pnode is not None:
                        leads_to_shiny_gold.add(pnode)
                    res = True

                if dfs(neigh[1], node):
                    leads_to_shiny_gold.add(pnode)
                    res = True

            return res
    dfs(input_node, None)

    return leads_to_shiny_gold


def count_all_bags(input_node):

    def traverse(node):
        total = 0

        for neigh in bag_graph[node[1]]:
            total += (neigh[0] + (neigh[0] * traverse(neigh)))
        return total

    sm = traverse((0, input_node))
    return sm


with open('7.txt', 'r') as f:
    lines = f.readlines()
    bag_graph = dict((process_line(ln) for ln in lines))

blsg_sets = [find_bags_leading_to_shiny_gold(node) for node in bag_graph.keys()]
blsg_set = set().union(*blsg_sets)
try:
    blsg_set.remove(None)
except KeyError:
    pass

print('P1: ', len(blsg_set))

sm = count_all_bags('shiny gold bag')
print('P2: ', sm)


