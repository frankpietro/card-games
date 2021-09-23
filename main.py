import random


class Deck:
    def __init__(self, card_number, card_array, card_values, suits_array):
        self.card_array = card_array
        self.card_values = card_values
        self.suits_array = suits_array

        self.cards = []
        self.build(card_number)
        self.shuffle()

    def build(self, card_number):
        for s in range(4):
            suit_number = int(card_number/len(self.suits_array))
            for v in range(suit_number):
                self.cards.append([v, s])

    def show_card(self, card):
        if 0 <= card[1] < 4:
            print(f"{self.card_array[card[0]]} of {self.suits_array[card[1]].lower()}")
        else:
            print("Jolly")

    def show(self):
        for card in self.cards:
            self.show_card(card)
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

    def draw(self, deck, sort_preference):
        secondary_preference = 0 if sort_preference else 1
        new_card = deck.draw_card()
        for i in range(len(self.hand)):
            if self.hand[i][sort_preference] > new_card[sort_preference] or self.hand[i][sort_preference] == new_card[sort_preference] and self.hand[i][secondary_preference] > new_card[secondary_preference]:
                self.hand.insert(i, new_card)
                return

        self.hand.insert(len(self.hand), new_card)

    def show_hand(self, deck):
        for card in self.hand:
            deck.show_card(card)
        print()


class Match:
    def __init__(self, players, card_number, card_array, card_values, suits_array):
        self.players = []
        for i in range(players):
            self.players.append(Player(i+1))

        self.deck = Deck(card_number, card_array, card_values, suits_array)

    def initial_draw(self, hand_number, sort_preference):
        for j in range(hand_number):
            for player in self.players:
                player.draw(self.deck, sort_preference)

    def show_game(self):
        for player in self.players:
            print("Player " + player.id)
            player.show_hand(self.deck)


class Tressette(Match):
    card_number = 40
    card_array = ['4', '5', '6', '7', 'J', 'Q', 'K', 'A', '2', '3']
    suits_array = ["Hearts", "Diamonds", "Clubs", "Spades"]
    card_values = [0, 0, 0, 0, 1/3, 1/3, 1/3, 1, 1/3, 1/3]
    sort_preference = 1  # sort by suit, then by number

    def __init__(self):
        super().__init__(2, self.card_number, self.card_array, self.card_values, self.suits_array)
        self.initial_draw(10, self.sort_preference)
        # for player in self.players:
        #     player.hand.sort(key=lambda x: (x[1], x[0]))


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

# m = Match(4, 52)
# m.initial_draw(3)
# m.show_game()

t = Tressette()
t.show_game()
