import os

import constants as c


def fraction_of_3(a):
    if abs(a - int(a)) < 0.0001:
        return f"{int(a)}"
    else:
        # if first decimal is 3, then it's 1/3
        if int(str(a)[2]) == 3:
            return f"{int(a)}.3"
        # if first decimal is 6, then it's 2/3
        elif int(str(a)[2]) == 6:
            return f"{int(a)}.6"
        

def select_winning_card(p1_card, p2_card):
    if p1_card.suit == p2_card.suit:
        if c.RANKS.index(p1_card.rank) < c.RANKS.index(p2_card.rank):
            return p2_card
    
    return p1_card


def print_sequence(sequence):
    p1_sequence = [sequence[0][0], c.PLACEHOLDER]
    p2_sequence = [c.PLACEHOLDER, sequence[1][0]]
    starter = 1
    for i in range(1, int(len(sequence)/2)):
        p1_card = sequence[2*(i-1)][0]
        p2_card = sequence[2*(i-1)+1][0]
        n1_card = sequence[2*(i-1)+2][0]
        n2_card = sequence[2*(i-1)+3][0]
        winner = select_winning_card(p1_card, p2_card)
        # print(f"Winning card: {winner}")
        if winner == p1_card and starter == 1 or winner == p2_card and starter == 2:
            p1_sequence.append(n1_card)
            p2_sequence.append(c.PLACEHOLDER)
            p1_sequence.append(c.PLACEHOLDER)
            p2_sequence.append(n2_card)
            starter = 1
        else:
            p1_sequence.append(c.PLACEHOLDER)
            p2_sequence.append(n1_card)
            p1_sequence.append(n2_card)
            p2_sequence.append(c.PLACEHOLDER)
            starter = 2

    for elem in p1_sequence:
        print(elem, end=" ")
    print()
    for elem in p2_sequence:
        print(elem, end=" ")
    print()


def is_allowed(tabled_card, card, hand):
    # card is not allowed if different suit than tabled card and hand has cards with same suit as tabled card
    if card.suit != tabled_card.suit:
        for c in hand:
            if c.suit == tabled_card.suit:
                # print(f"Not allowed: {tabled_card} {card} with hand {hand} because of {c}")
                return False

    # print(f"Allowed: {tabled_card} {card} with hand {hand}")
    return True


def create_dir_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def remove_dir(folder):
    if os.path.exists(folder):
        # remove all files in folder
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
        os.rmdir(folder)


def path_from_hands(p1_hand, p2_hand):
    # create string with all cards of p1_hand and all of p2_hand
    path_name = ""
    
    for card in p1_hand:
        path_name += card.name
    
    path_name += "_"
    
    for card in p2_hand:
        path_name += card.name

    return path_name