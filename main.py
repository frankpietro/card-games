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




def run(self, p1_hand, p2_hand, p1_score, p2_score, turn, tabled_card=None, verbose=0):
    turn_hand, other_hand = u.select_turn_hand(p1_hand, p2_hand, turn)

    if not tabled_card:
        path = u.path_from_hands(turn_hand, other_hand)
        filename = f"{c.TEMP_DIR}/{path}.pkl"

        if os.path.exists(filename):
            with open(filename, "rb") as f:
                best_scores, best_sequence = pkl.load(f)

                return best_scores, best_sequence

        best_scores = [0,0]
        best_sequence = None
        for card in p1_hand:
            p1_copy = p1_hand.copy()
            p2_copy = p2_hand.copy()
            p1_score_copy = p1_score
            p2_score_copy = p2_score
            
            if verbose:
                print(f"p1_hand: {p1_hand}; p2_hand: {p2_hand}")
                print(f"Score: {u.fraction_of_3(p1_score)} {u.fraction_of_3(p2_score)}")
                print(f"Playing {card}")

            p1_copy.remove(card)
            scores, sequence = self.run(p1_copy, p2_copy, p1_score_copy, p2_score_copy, card, verbose)

            if scores[0] > best_scores[0]:
                # if verbose:
                #     print(f"New best scores: {scores} with card {card}")
                #     print(f"Previous best scores: {best_scores} with card {best_sequence}")
                best_scores = scores
                best_sequence = sequence
                best_sequence.insert(0, card)

        if verbose:
            # print(f"Returning best scores: {best_scores} and best sequence: {best_sequence}")
            # print()
            # print()
            print(f"Score: {u.fraction_of_3(best_scores[0])} {u.fraction_of_3(best_scores[1])} with ")
            u.print_sequence(best_sequence)
        
        # save best scores and best sequence to file using pickle
        with open(filename, "wb") as f:
            pkl.dump((best_scores, best_sequence), f)
                    
        return best_scores, best_sequence
            
    else:
        path = u.path_from_hands(p1_hand, p2_hand)
        filename = f"{c.TEMP_DIR}/{path}.pkl"
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                best_scores, best_sequence = pkl.load(f)

                return best_scores, best_sequence

        best_scores = [0,0]
        best_sequence = None
        for card in p2_hand:
            if u.is_allowed(tabled_card, card, p2_hand):
                print(f"Allowed: {tabled_card} {card} with hand {p2_hand}")
                p1_copy = p1_hand.copy()
                p2_copy = p2_hand.copy()
                p1_score_copy = p1_score
                p2_score_copy = p2_score
                
                if verbose:
                    print(f"p1_hand: {p1_hand}; p2_hand: {p2_hand}")
                    print(f"Tabled card: {tabled_card}")
                    print(f"Score: {u.fraction_of_3(p1_score)} {u.fraction_of_3(p2_score)}")
                    print(f"Playing {card}")
                
                p2_copy.remove(card)
                winning_card = u.select_winning_card(tabled_card, card)
                
                if verbose:
                    print(f"Table: {tabled_card} {card}; winner: {winning_card}")
                
                if winning_card == card:
                    p2_score_copy += card.value + tabled_card.value
                else:
                    p1_score_copy += card.value + tabled_card.value

                if len(p1_hand) == 0:
                    p1_score_copy += winning_card != card
                    p2_score_copy += winning_card == card
                    return [p1_score_copy, p2_score_copy], [card]
                
                if winning_card != card:
                    scores, sequence = self.run(p1_copy, p2_copy, p1_score_copy, p2_score_copy, verbose=verbose)
                else:
                    scores, sequence = self.run(p2_copy, p1_copy, p2_score_copy, p1_score_copy, verbose=verbose)
                    # invert scores
                    scores = [scores[1], scores[0]]
                
                if scores[1] > best_scores[1]:
                    # if verbose:
                    #     print(f"New best scores: {scores} with card {card}")
                    #     print(f"Previous best scores: {best_scores} with card {sequence}")
                    best_scores = scores
                    best_sequence = sequence
                    best_sequence.insert(0, card)

        with open(filename, "wb") as f:
            pkl.dump((best_scores, best_sequence), f)

        return best_scores, best_sequence