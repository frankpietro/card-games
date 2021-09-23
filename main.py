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
            for v in card_numbers[str(card_number)]:
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
        self.id = str(player_id)
        self.hand = []
        self.own = []

    def draw(self, deck):
        self.hand.append(deck.draw_card())

    def show_hand(self):
        for card in self.hand:
            card.show()
        print()


class Match:
    def __init__(self, players, card_number):
        self.players = []
        for i in range(players):
            self.players.append(Player(i+1))

        self.deck = Deck(card_number)

    def initial_draw(self, hand_number):
        for j in range(hand_number):
            for player in self.players:
                player.draw(self.deck)

    def show_game(self):
        for player in self.players:
            print("Player " + player.id)
            player.show_hand()


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

# d = Deck('52')
# p = Player(1)
# p.draw(d)
# p.show_hand()

m = Match(4, 52)
m.initial_draw(3)
m.show_game()
