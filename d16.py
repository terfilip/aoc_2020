import re
from collections import defaultdict
from copy import deepcopy

import numpy as np

rgx = re.compile('([a-z\s]+):\s(\d+)-(\d+) or (\d+)-(\d+)')


def read_in(fname):

    with open(fname, 'r') as f:
        ticket_ranges = {}
        nearby_tickets = []

        while line := f.readline():
            line = line.strip()

            if line == '':
                continue
            elif line == 'your ticket:':
                your_ticket = list(map(int, f.readline().strip().split(',')))
            elif line == 'nearby tickets:':
                break
            else:
                match = rgx.match(line)
                ticket_ranges[match.group(1)] = tuple(int(match.group(i)) for i in (2, 3, 4, 5))

        while line := f.readline():
            nearby_tickets.append(list(map(int, line.strip().split(','))))
        return ticket_ranges, your_ticket, nearby_tickets


ticket_ranges, your_ticket, nearby_tickets = read_in('16.txt')
ticket_ranges_s1, your_ticket_s1, nearby_tickets_s1 = read_in('16sample1.txt')
ticket_ranges_s2, your_ticket_s2, nearby_tickets_s2 = read_in('16sample2.txt')


def ticket_in_range(ticket, lb0, ub0, lb1, ub1):
    return (lb0 <= ticket <= ub0) or (lb1 <= ticket <= ub1)


def all_tickets_in_range(tickets, ranges):
    return all(ticket_in_range(ticket, *ranges) for ticket in tickets)


def ticket_in_any_range(ticket, ticket_ranges):
    return any((ticket_in_range(ticket, lb0, ub0, lb1, ub1) for (lb0, ub0, lb1, ub1) in ticket_ranges.values()))


def p1(ticket_ranges, tickets):
    invalid_tickets = [ticket for sub in tickets for ticket in sub
                       if not ticket_in_any_range(ticket, ticket_ranges)]
    return sum(invalid_tickets)


def p2(ticket_ranges, your_ticket, tickets):
    category2tickets = defaultdict(list)
    category2ticket = {}
    ticket_ranges = deepcopy(ticket_ranges)
    valid_tickets = [row for row in tickets if all(ticket_in_any_range(t, ticket_ranges) for t in row)]

    for i, ticket in enumerate(your_ticket):
        col = [row[i] for row in valid_tickets]

        for k, v in ticket_ranges.items():
            if all_tickets_in_range(col, v):
                category2tickets[k].append(ticket)

    while len(category2tickets):
        minlen = min(len(v) for v in category2tickets.values())
        min_key, min_val = [(k, v) for k, v in category2tickets.items() if len(v) == minlen][0]
        min_val = min_val[0]
        category2ticket[min_key] = category2tickets.pop(min_key)[0]

        for k, v in category2tickets.items():
            try:
                v.remove(min_val)
            except ValueError:
                print(f'value {min_val} not in list')

    ans = np.prod([v for k, v in category2ticket.items() if k.startswith('departure')])
    return ans, category2ticket


print('P1 :', p1(ticket_ranges, nearby_tickets))
print('P2 :', p2(ticket_ranges, your_ticket, nearby_tickets)[0])
