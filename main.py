import random

from card import Card, TressetteDeck, StatefulCard
from tressette import Tressette
from player import Player

import constants as c
import utilities as u


# initialize game
t = Tressette()

p1 = t.players[0]
p2 = t.players[1]

c1 = Card("3", c.SPADES)
c2 = Card("2", c.SPADES)
c3 = Card("A", c.SPADES)
c4 = Card("K", c.SPADES)
c5 = Card("Q", c.SPADES)
c6 = Card("J", c.SPADES)
# c7 = Card("7", c.SPADES)
# c8 = Card("6", c.SPADES)
# c9 = Card("5", c.SPADES)
# c10 = Card("4", c.SPADES)

# cards = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
cards = [c6, c5, c1, c4, c2, c3]

# random.shuffle(cards)

for card in cards[:3]:
    p1.receive_card(card)
    p2.add_opponent_card(card)

for card in cards[3:]:
    p2.receive_card(card)
    p1.add_opponent_card(card)

print(f"{p1.name} hand: {p1.hand}")
print(f"{p2.name} hand: {p2.hand}")

scores, sequence = t.run(p1.hand.copy(), p2.hand.copy(), 0, 0, verbose=1)

print(f"{p1.name} score: {u.fraction_of_3(scores[0])}")
print(f"{p2.name} score: {u.fraction_of_3(scores[1])}")

u.print_sequence(sequence)