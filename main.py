import random

card_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
card_numbers = {'52': ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'],
                '40': ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'],
                '54': ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']}


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.name = f"{value}{suit[0]}"

    def show(self):
        print(f"{self.value} of {self.suit.lower()}") if self.suit else print("Jolly")


class Deck:
    def __init__(self, number):
        self.cards = []
        self.build(number)
        self.shuffle()

    def build(self, card_number):
        for s in card_suits:
            for v in card_numbers[card_number]:
                self.cards.append(Card(v, s))

    def show(self):
        for card in self.cards:
            card.show()
        print()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()


class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.hand = []

    def draw(self, deck):
        self.hand.append(deck.draw_card())

    def show_hand(self):
        for card in self.hand:
            card.show()
        print()


# c = Card("J", "Diamonds")
# c.show()


# d = Deck('40')
# d.show()
# c1 = d.draw_card()
# c1.show()
# print()
# c2 = d.draw_card()
# c2.show()
# print()
# d.show()

d = Deck('52')
p = Player(1)
p.draw(d)
p.show_hand()
