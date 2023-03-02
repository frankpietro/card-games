from card import StatefulDeck

import constants as c


class Player(object):
    def __init__(self, name, initial_score=0, initial_game_score=0):
        self.hand = []
        self.game_score = initial_game_score

        self.score = initial_score
        self.name = name

        self.information_deck = StatefulDeck()
        self.information_deck.create_deck()

    
    def __str__(self):
        return self.name


    def draw(self, deck):
        drawn_card = deck.draw_card()
        self.hand.append(drawn_card)
        self.hand.sort()
        return drawn_card


    def show_hand(self):
        for card in self.hand:
            print(card, end=' ')
        print()

        
    def set_hand(self, hand):
        self.hand = hand


    def receive_card(self, card):
        # append card to hand
        self.hand.append(card)
        # sort hand
        self.hand.sort()
        # update state of card
        self.add_own_card(card)


    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        else:
            # print an error message
            print("Card not in hand")
            # return None
            return None


    def select_card(self, tabled_card=None):
        # select a card from the hand
        
        selected_card = self.hand[0]
        # returns that card
        return selected_card
    

    def add_final_bonus(self, bonus=c.FINAL_HAND_BONUS):
        self.score += bonus


    def end_set(self):
        set_score = int(self.score)
        self.game_score += set_score
        self.score = 0
        return set_score


    # utility functions to be removed later
    def change_card_state(self, card, state):
        stateful_card = self.information_deck.get_card(card)
        stateful_card.state = state


    def add_own_card(self, card):
        self.change_card_state(card, c.PLAYER_HAND)

    
    def add_opponent_card(self, card):
        self.change_card_state(card, c.OPPONENT_HAND)

    
    def add_taken_card(self, card):
        self.change_card_state(card, c.PLAYER_TAKEN)


    def add_opp_taken_card(self, card):
        self.change_card_state(card, c.OPPONENT_TAKEN)


    def retrieve_opponent_hand(self):
        opponent_hand = []
        for card in self.information_deck.cards:
            if card.state == c.OPPONENT_HAND:
                opponent_hand.append(card)
        return opponent_hand