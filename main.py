import random


class Deck:
    cards = []

    def __init__(self, card_number, card_array, suits_array):
        self.card_array = card_array
        self.suits_array = suits_array
        self.reset(card_number)

    def reset(self, card_number):
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
            print(f"{self.card_array[card[0]]}{self.suits_array[card[1]][0]}")
            # print(f"{self.card_array[card[0]]} of {self.suits_array[card[1]].lower()}")
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
    def __init__(self, player_id, score, match_score):
        self.id = str(player_id)
        self.hand = []
        self.own = []
        self.score = score
        self.match_score = match_score

    def draw(self, deck, sort_preference):
        if not deck.cards:
            return

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
    def __init__(self, players, card_number, card_array, suits_array, initial_score, initial_match_score):
        self.players = []
        for i in range(players):
            self.players.append(Player(i+1, initial_score, initial_match_score))

        self.deck = Deck(card_number, card_array, suits_array)

    def initial_draw(self, hand_number, sort_preference):
        for j in range(hand_number):
            for player in self.players:
                player.draw(self.deck, sort_preference)

    def show_game(self):
        for player in self.players:
            if player.hand:
                print("Player " + player.id)
                player.show_hand(self.deck)
                return
            else:
                print(f"Player {player.id}: {int(player.score)}")
        print()


class Tressette(Match):
    card_number = 40
    card_array = ['4', '5', '6', '7', 'J', 'Q', 'K', 'A', '2', '3']
    suits_array = ["Hearts", "Diamonds", "Clubs", "Spades"]
    card_values = [0, 0, 0, 0, 1/3, 1/3, 1/3, 1, 1/3, 1/3]
    sort_preference = 1  # sort by suit, then by number
    max_turns = 20
    initial_score = 0
    initial_match_score = 0
    max_match_score = 21
    turn_number = 0
    first = 0

    def __init__(self):
        super().__init__(2, self.card_number, self.card_array, self.suits_array, self.initial_score, self.initial_match_score)
        self.reset_game()

    def reset_game(self):
        self.turn_number = 0
        self.first = random.randint(0, 1)

        for player in self.players:
            player.own = []
            player.hand = []

        self.deck.reset(self.card_number)

        self.initial_draw(10, self.sort_preference)

    def select_card(self, card, hand):
        same_suit = []
        for i in range(len(hand)):
            if hand[i][1] == card[1]:
                same_suit.append(i)
        if not same_suit:
            return random.randint(0, len(self.players[(self.first+1) % 2].hand)-1)
        random.shuffle(same_suit)
        return same_suit[0]

    def take_card(self, player_index, card):
        self.players[player_index].own.insert(len(self.players[player_index].own), card)

    def play_turn(self):
        self.turn_number += 1

        # first player plays
        first_card_index = random.randint(0, len(self.players[self.first].hand)-1)
        first_card = self.players[self.first].hand.pop(first_card_index)

        # second player plays
        second_card_index = self.select_card(first_card, self.players[(self.first+1) % 2].hand)
        second_card = self.players[(self.first+1) % 2].hand.pop(second_card_index)

        # show plays
        print("Turn " + str(self.turn_number))
        print("Player " + self.players[self.first].id)
        self.deck.show_card(first_card)
        print("Player " + self.players[(self.first+1) % 2].id)
        self.deck.show_card(second_card)
        print()

        # one of them takes the hand
        if second_card[1] != first_card[1]:
            self.take_card(self.first, first_card)
            self.take_card(self.first, second_card)
        else:
            if second_card[0] < first_card[0]:
                self.take_card(self.first, first_card)
                self.take_card(self.first, second_card)
            else:
                self.take_card((self.first+1) % 2, first_card)
                self.take_card((self.first+1) % 2, second_card)
                self.first = (self.first+1) % 2

        self.players[self.first].score = self.players[self.first].score + self.card_values[first_card[0]] + self.card_values[second_card[0]]
        if self.turn_number == self.max_turns:
            self.players[self.first].score += 1

        # both players draw a card
        for player in self.players:
            player.draw(self.deck, self.sort_preference)

    def simulate_game(self):
        while self.turn_number < self.max_turns:
            self.play_turn()
            self.show_game()

        game_over = 0
        for player in self.players:
            player.match_score += int(player.score + 0.1)
            player.score = self.initial_score
            game_over += (player.match_score >= self.max_match_score)

        return game_over
        # self.reset_game()

    def show_final_result(self):
        print("Game over")
        for player in self.players:
            print(f"Player {player.id}: {int(player.match_score)}")
        self.players.sort(key=lambda x: x.match_score, reverse=True)
        print(f"The winner is player {self.players[0].id}")

    def simulate_match(self):
        while not self.simulate_game():
            self.reset_game()

        self.show_final_result()


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
t.simulate_match()
