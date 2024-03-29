from card import TressetteDeck
from player import Player
import pickle as pkl
import os

import constants as c
import utilities as u


class Tressette(object):
    def __init__(self):
        self.players = [
            Player(c.P1),
            Player(c.P2)
        ]

        self.deck = TressetteDeck()
        self.player_turn = 0
        self.player_set_turn = 0


    def initial_draw(self):
        for player in self.players:
            for i in range(c.STARTING_HAND):
                player.draw(self.deck)


    def ack_turn(self, p1_card, p2_card):
        winning_card = u.select_winning_card(p1_card, p2_card)

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

    
    def draw(self, verbose=False):
        p1 = self.players[self.player_turn]
        p2 = self.players[(self.player_turn+1)%2]
        
        p1_card = p1.draw(self.deck)
        p2_card = p2.draw(self.deck)
        
        if verbose:
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


    def run(self, p1_hand, p2_hand, p1_score, p2_score, turn, tabled_card=None, verbose=0):
        [turn_hand, other_hand] = [p1_hand, p2_hand] if turn == 0 else [p2_hand, p1_hand]

        if not tabled_card:
            best_scores, best_sequence, found, filename = u.search_ready_solution(turn_hand, other_hand)
            if found:
                return best_scores, best_sequence

            for card in turn_hand:
                p1_hand_copy = p1_hand.copy()
                p2_hand_copy = p2_hand.copy()
                [turn_hand_copy, _] = [p1_hand_copy, p2_hand_copy] if turn == 0 else [p2_hand_copy, p1_hand_copy]
                p1_score_copy = p1_score
                p2_score_copy = p2_score
                turn_copy = turn
                         
                u.print_state(turn_hand, other_hand, p1_score, p2_score, turn, card, verbose)

                # play card
                turn_hand_copy.remove(card)

                # let the other player decide their move
                turn_copy = (turn_copy+1)%2
                scores, sequence = self.run(p1_hand_copy, p2_hand_copy, p1_score_copy, p2_score_copy, turn_copy, card, verbose)

                if scores[turn] >= best_scores[turn]:
                    best_scores = scores
                    best_sequence = sequence
                    best_sequence.insert(0, (card, turn))

            u.print_score_sequence(best_scores, best_sequence, verbose)
            
            u.save_solution(filename, best_scores, best_sequence)
                      
            return best_scores, best_sequence
                
        else:
            best_scores, best_sequence, found, filename = u.search_ready_solution(turn_hand, other_hand, tabled_card)
            if found:
                return best_scores, best_sequence
                
            for card in turn_hand:
                if u.is_allowed(tabled_card, card, turn_hand, verbose):
                    p1_hand_copy = p1_hand.copy()
                    p2_hand_copy = p2_hand.copy()
                    [turn_hand_copy, _] = [p1_hand_copy, p2_hand_copy] if turn == 0 else [p2_hand_copy, p1_hand_copy]
                    p1_score_copy = p1_score
                    p2_score_copy = p2_score
                    turn_copy = turn

                    u.print_state(turn_hand, other_hand, p1_score, p2_score, turn, card, verbose, tabled_card)

                    # play card
                    turn_hand_copy.remove(card)
                    
                    winning_card = u.select_winning_card(tabled_card, card, verbose)
                    
                    # winner: p2 if they played the last card and it is winning or if now p1 played the losing card
                    if winning_card == card and turn_copy == 1 or winning_card == tabled_card and turn_copy == 0:
                        p2_score_copy += card.value + tabled_card.value
                    else:
                        p1_score_copy += card.value + tabled_card.value

                    if len(other_hand) == 0:
                        if verbose:
                            print(f"End of computations")
                        
                        if winning_card == card and turn_copy == 1 or winning_card == tabled_card and turn_copy == 0:
                            p2_score_copy += 1
                        else:
                            p1_score_copy += 1
                        return [p1_score_copy, p2_score_copy], [(card, turn)]
                    
                    # if second person won, they start, so turn does not change, otherwise it does
                    if winning_card != card:
                        turn_copy = (turn_copy+1)%2
                    
                    scores, sequence = self.run(p1_hand_copy, p2_hand_copy, p1_score_copy, p2_score_copy, turn_copy, verbose=verbose)

                    if scores[turn] >= best_scores[turn]:
                        best_scores = scores
                        best_sequence = sequence
                        best_sequence.insert(0, (card, turn))

            u.print_score_sequence(best_scores, best_sequence, verbose, tabled_card)

            u.save_solution(filename, best_scores, best_sequence)

            return best_scores, best_sequence
                