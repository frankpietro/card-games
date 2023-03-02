from card import TressetteDeck
from player import Player

import constants as c


class Tressette(object):
    def __init__(self, deck=TressetteDeck(), draw=False):
        self.players = [
            Player(c.P1),
            Player(c.P2)
        ]

        self.deck = deck
        self.player_turn = 0
        self.player_set_turn = 0


    def initial_draw(self):
        for player in self.players:
            for i in range(c.STARTING_HAND):
                player.draw(self.deck)


    def select_winning_card(self, p1_card, p2_card):
        if p1_card.suit == p2_card.suit:
            if c.RANKS.index(p1_card.rank) < c.RANKS.index(p2_card.rank):
                return p2_card
        
        return p1_card


    def ack_turn(self, p1_card, p2_card):
        winning_card = self.select_winning_card(p1_card, p2_card)
        print(f"Winning card is {winning_card}")

        # who wins the hand starts the next turn
        if winning_card == p2_card:
            self.player_turn = (self.player_turn+1)%2

        winner = self.player_turn
        loser = (self.player_turn+1)%2

        self.players[winner].add_taken_card(p1_card)
        self.players[winner].add_taken_card(p2_card)

        self.players[loser].add_opp_taken_card(p1_card)
        self.players[loser].add_opp_taken_card(p2_card)

        self.players[winner].score += p1_card.value + p2_card.value


    def play_turn(self, tabled_card=None):
        print(f"{self.players[self.player_turn].name}'s turn")
        card_to_play = self.players[self.player_turn].select_card(tabled_card)
        played_card = self.players[self.player_turn].play_card(card_to_play)
        print(f"Player {self.players[self.player_turn].name} played {played_card}")
        self.player_turn = (self.player_turn+1)%2
        return played_card

    
    def draw(self):
        p1 = self.players[self.player_turn]
        p2 = self.players[(self.player_turn+1)%2]
        
        p1_card = p1.draw(self.deck)
        p2_card = p2.draw(self.deck)
        
        print(f"Player {p1.name} drew {p1_card}")
        print(f"Player {p2.name} drew {p2_card}")
        
        p1.add_opponent_card(p2_card)
        p2.add_opponent_card(p1_card)


    def ack_set(self):
        # for each player, add score to game score as an integer
        set_scores = []

        for p in self.players:
            set_scores.append(p.end_set())
        
        self.player_set_turn = (self.player_set_turn+1)%2
        self.player_turn = self.player_set_turn

        return set_scores

    
    def turn(self):
        p1_card = self.play_turn()
        p2_card = self.play_turn(p1_card)

        print(f"Table: {p1_card} {p2_card}")

        self.ack_turn(p1_card, p2_card)

        print(f"Score: {self.players[0].score} {self.players[1].score}")

        if len(self.deck.cards) != 0:
            print("Players draw")
            self.draw()

        if len(self.players[0].hand) == 0:
            print("Game finished")
            self.players[self.player_turn].add_final_bonus()
            set_scores = self.ack_set()
            print(f"Set score: {set_scores[0]} {set_scores[1]}")
            print(f"Total score: {self.players[0].game_score} {self.players[1].game_score}")
            return set_scores
        else:
            print("Next turn")

        return None


    def run(self, p1_hand, p2_hand, p1_score, p2_score, tabled_card=None, verbose=0):
        if not tabled_card:
            best_scores = [0,0]
            best_sequence = None
            for card in p1_hand:
                p1_copy = p1_hand.copy()
                p2_copy = p2_hand.copy()
                p1_score_copy = p1_score
                p2_score_copy = p2_score
                if verbose:
                    print(f"p1_hand: {p1_hand}")
                    print(f"p2_hand: {p2_hand}")
                    print(f"p1_score: {p1_score}")
                    print(f"p2_score: {p2_score}")
                    print(f"Playing {card}")
                p1_copy.remove(card)
                scores, sequence = self.run(p1_copy, p2_copy, p1_score_copy, p2_score_copy, card)
                if verbose:
                    print(f"Scores: {scores}")
                if scores[0] >= best_scores[0]:
                    if verbose:
                        print(f"New best scores: {scores} with card {card}")
                        print(f"Previous best scores: {best_scores} with card {best_sequence}")
                    best_scores = scores
                    best_sequence = sequence
                    best_sequence.insert(0, card)

            if verbose:
                print(f"Returning best scores: {best_scores} and best sequence: {best_sequence}")
                print()
                print()
            return best_scores, best_sequence
                
        else:
            best_scores = [0,0]
            best_sequence = None
            for card in p2_hand:
                p1_copy = p1_hand.copy()
                p2_copy = p2_hand.copy()
                p1_score_copy = p1_score
                p2_score_copy = p2_score
                if verbose:
                    print(f"p1_hand: {p1_hand}")
                    print(f"p2_hand: {p2_hand}")
                    print(f"Tabled card: {tabled_card}")
                    print(f"p1_score: {p1_score}")
                    print(f"p2_score: {p2_score}")
                    print(f"Playing {card}")
                p2_copy.remove(card)
                winning_card = self.select_winning_card(tabled_card, card)
                if verbose:
                    print(f"Table: {tabled_card} {card}")
                    print(f"Winner: {winning_card}")
                if winning_card == card:
                    p2_score_copy += card.value + tabled_card.value
                else:
                    p1_score_copy += card.value + tabled_card.value

                if len(p1_hand) == 0:
                    p1_score_copy += winning_card != card
                    p2_score_copy += winning_card == card
                    return [p1_score_copy, p2_score_copy], [card]
                
                if winning_card != card:
                    scores, sequence = self.run(p1_copy, p2_copy, p1_score_copy, p2_score_copy)
                else:
                    scores, sequence = self.run(p2_copy, p1_copy, p2_score_copy, p1_score_copy)
                    # invert scores
                    scores = [scores[1], scores[0]]
                
                if scores[1] >= best_scores[1]:
                    if verbose:
                        print(f"New best scores: {scores} with card {card}")
                        print(f"Previous best scores: {best_scores} with card {sequence}")
                    best_scores = scores
                    best_sequence = sequence
                    best_sequence.insert(0, card)

            if verbose:
                print(f"Returning best scores: {best_scores} and best sequence: {best_sequence}")
                print()
                print()
            
            return best_scores, best_sequence
                