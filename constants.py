HEARTS = "hearts"
DIAMONDS = "diamonds"
CLUBS = "clubs"
SPADES = "spades"

SUITS = [HEARTS, DIAMONDS, CLUBS, SPADES]

TRESSETTE = {
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "J": 1/3,
    "Q": 1/3,
    "K": 1/3,
    "A": 1,
    "2": 1/3,
    "3": 1/3
}

RANKS = list(TRESSETTE.keys())
VALUES = list(TRESSETTE.values())

P1 = "X"
P2 = "GT"

STARTING_HAND = 10
FINAL_HAND_BONUS = 1


# CARD STATES
# -1: unknown
UNKNOWN = -1
# 0: in the deck
DECK = 0
# 1: in the hand of the other player
OPPONENT_HAND = 1
# 2: in the hand of the player
PLAYER_HAND = 2
# 3: taken by the other player
OPPONENT_TAKEN = 3
# 4: taken by the player
PLAYER_TAKEN = 4