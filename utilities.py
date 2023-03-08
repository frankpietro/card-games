import os
import pickle as pkl

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
        

def select_winning_card(tabled_card, card, verbose=False):
    if tabled_card.suit == card.suit:
        if c.RANKS.index(tabled_card.rank) < c.RANKS.index(card.rank):
            w = card
        else:
            w = tabled_card
    else:
        w = tabled_card

    if verbose:
        print(f"Table: {tabled_card} {card}; winner: {w}")
    
    return w


def print_sequence(sequence, tabled_card=None):
    if tabled_card is not None:
        sequence = [(tabled_card, -1)] + sequence

    if sequence[1][1] == 1:
        p1_sequence = [sequence[0][0], c.PLACEHOLDER]
        p2_sequence = [c.PLACEHOLDER, sequence[1][0]]
    else:
        p1_sequence = [c.PLACEHOLDER, sequence[1][0]]
        p2_sequence = [sequence[0][0], c.PLACEHOLDER]

    if len(sequence) > 2:
        for i in range(2, len(sequence)):
            if sequence[i][1] == 0:
                p1_sequence.append(sequence[i][0])
                p2_sequence.append(c.PLACEHOLDER)
            else:
                p1_sequence.append(c.PLACEHOLDER)
                p2_sequence.append(sequence[i][0])

    for elem in p1_sequence:
        print(elem, end=" ")
    print()
    for elem in p2_sequence:
        print(elem, end=" ")
    print()


def is_allowed(tabled_card, card, hand, verbose=False):
    # card is not allowed if different suit than tabled card and hand has cards with same suit as tabled card
    if card.suit != tabled_card.suit:
        for c in hand:
            if c.suit == tabled_card.suit:
                if verbose:
                    print(f"Not allowed: {tabled_card} {card} with hand {hand} because of {c}")
                return False

    if verbose:
        print(f"Allowed: {tabled_card} {card} with hand {hand}")
    
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


def path_from_hands(p1_hand, p2_hand, tabled_card):
    # create string with all cards of p1_hand and all of p2_hand
    path_name = ""
    
    for card in p1_hand:
        path_name += card.name
    
    path_name += "_"
    
    for card in p2_hand:
        path_name += card.name

    if tabled_card:
        path_name += f"_{tabled_card.name}"

    return path_name


def print_state(turn_hand, other_hand, p1_score, p2_score, turn, card, verbose, tabled_card=None):
    if verbose:
        print(f"Turn hand: {turn_hand}; other hand: {other_hand}")
        print(f"Score: {fraction_of_3(p1_score)} {fraction_of_3(p2_score)}")
        if tabled_card:
            print(f"Tabled card: {tabled_card}")
        print(f"Player {turn} playing {card}")


def print_score_sequence(best_scores, best_sequence, verbose, tabled_card=None):
    if verbose:
        print(f"Best score for player {best_sequence[0][1]}: {fraction_of_3(best_scores[0])} {fraction_of_3(best_scores[1])} with ")
        print_sequence(best_sequence, tabled_card)


def search_ready_solution(turn_hand, other_hand, tabled_card=None):
    path = path_from_hands(turn_hand, other_hand, tabled_card)
    filename = f"{c.TEMP_DIR}/{path}.pkl"

    # if solution already computed, go on
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            best_scores, best_sequence = pkl.load(f)

            return best_scores, best_sequence, True, filename

    return [0,0], None, False, filename


def save_solution(filename, best_scores, best_sequence):
    with open(filename, "wb") as f:
        pkl.dump((best_scores, best_sequence), f)