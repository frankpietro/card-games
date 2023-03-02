import random
import constants as c


class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = c.TRESSETTE[rank]
        
        self.name = rank + suit[0]


    def __str__(self):
        return self.name

    
    def __repr__(self):
        return self.name


    def __eq__(self, other):
        return self.name == other.name

    
    def __lt__(self, other):
        # suits are ordered as: hearts, diamonds, clubs, spades
        # ranks are ordered as in c.TRESSETTE
        if self.suit == other.suit:
            # position of rank in c.TRESSETTE
            return c.RANKS.index(self.rank) < c.RANKS.index(other.rank)
        else:
            return c.SUITS.index(self.suit) < c.SUITS.index(other.suit)


class StatefulCard(Card):
    def __init__(self, rank, suit):
        super().__init__(rank, suit)

        self.relative_rank = rank
        self.state = c.UNKNOWN


    def __str__(self):
        return self.name + " " + str(self.state)
    

    def __repr__(self):
        return self.name + " " + str(self.state)
    

class TressetteDeck(object):
    def __init__(self, suits=c.SUITS):
        self.suits = suits
        self.ranks = c.RANKS
        self.values = c.VALUES
        self.cards = []


    def create_deck(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(rank, suit))


    def shuffle(self):
        random.shuffle(self.cards)


    def draw_card(self):
        return self.cards.pop()


    def show_deck(self):
        for card in self.cards:
            print(card, end=' ')
        print()


class StatefulDeck(TressetteDeck):
    def __init__(self, suits=c.SUITS):
        super().__init__(suits)


    def create_deck(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(StatefulCard(rank, suit))


    def get_card(self, card):
        for c in self.cards:
            if c == card:
                return c