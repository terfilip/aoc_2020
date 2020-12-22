from collections import deque
from copy import copy


def read_in(fname):
    deck1 = deque()
    deck2 = deque()

    with open(fname, 'r') as f:
        is2 = False

        while line := f.readline():
            line = line.strip()
            if line == '' or line.startswith('Player 1'):
                continue

            if line.startswith('Player 2'):
                is2 = True
            elif not is2:
                deck1.append(int(line))
            elif is2:
                deck2.append(int(line))
    return deck1, deck2


def play_game(deck1, deck2):

    while len(deck1) and len(deck2):
        p1card = deck1.popleft()
        p2card = deck2.popleft()

        if p1card > p2card:
            deck1.append(p1card)
            deck1.append(p2card)
        elif p2card > p1card:
            deck2.append(p2card)
            deck2.append(p1card)
        else:
            raise ValueError("Drawn cards should never be equal")

    return deck1 if len(deck1) else deck2


def play_rec_game_helper(deck1, deck2):
    round_history = []

    while len(deck1) and len(deck2):

        if (deck1, deck2) in round_history:
            return deck1, deck2, 1
        round_history.append((copy(deck1), copy(deck2)))
        p1card = deck1.popleft()
        p2card = deck2.popleft()

        if len(deck1) >= p1card and len(deck2) >= p2card:
            d1sub = deque(list(deck1)[:p1card])
            d2sub = deque(list(deck2)[:p2card])
            _, _, winner = play_rec_game_helper(d1sub, d2sub)

            if winner == 1:
                deck1.append(p1card)
                deck1.append(p2card)
            elif winner == 2:
                deck2.append(p2card)
                deck2.append(p1card)
            else:
                raise ValueError('winner must be 1 or 2')
        else:
            if p1card > p2card:
                deck1.append(p1card)
                deck1.append(p2card)
            elif p2card > p1card:
                deck2.append(p2card)
                deck2.append(p1card)
            else:
                raise ValueError("Drawn cards should never be equal")
    winner = 1 if len(deck1) else 2
    return deck1, deck2, winner


def play_rec_game(deck1, deck2):
    # Runs for a long time but it's not infinite recursion
    deck1, deck2, winner = play_rec_game_helper(copy(deck1), copy(deck2))
    windeck = deck1 if winner == 1 else deck2
    return windeck


def count_winning_score(indeck1, indeck2, play_game):
    windeck = play_game(copy(indeck1), copy(indeck2))
    return sum([(i + 1) * card for i, card in enumerate(reversed(list(windeck)))])


s1deck1, s1deck2 = read_in('22sample1.txt')
deck1, deck2 = read_in('22.txt')
print('P1: ', count_winning_score(deck1, deck2, play_game))
print('P2: ', count_winning_score(deck1, deck2, play_rec_game))