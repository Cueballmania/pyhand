# The strategy to create the dictionaries for the 7 card evaluator is to 
# first run the 5 card evaluator to create a dictionary of all 5 card hands
# then iterate all of the 7 card hands to map them to the best 5 card hand they can make
# each of these are stored in the correct place
import deck
import itertools
import collections
import pickle
from card import Card
from typing import List
import evaluator as e

def pickle_dict(filename: str, dict: dict):
    # This function will pickle the dictionary
    with open(filename, 'wb') as f:
        pickle.dump(dict, f, protocol=pickle.HIGHEST_PROTOCOL)

# Get the suit string from each card
def _small_suit_calc(card: Card) -> int:
    return (card.get_int_rep() & 61440) >> 12

# Count the number of suits in the hand and return the greatest
# Ties do not matter since the highest tie is 3/3/1 and a flush can only occur with 5 or more
def _n_suit(cards: List[Card]) -> int:
    suit_cnt = collections.Counter([_small_suit_calc(card) for card in cards])
    (small_suit, num) = suit_cnt.most_common(1)[0]
    return num

if __name__ == "__main__":

    d = deck.Deck()
    five_card_strength = {} # caching the hand value for use in 7-card validation
    for hand in itertools.combinations(d.cards,5):
        five_card_strength[hand] = e.evaluate_hand(hand)

    # Generate the flush67_dict
    # Observe that you only need to iterate through one suit's cards
    # finding all 6 card combos is equivalent to finding all 7 card combos
    # since 13C7 = 13C6
    flush67_dict = {}
    suit_deck = d.cards[0:13]

    for hand in itertools.combinations(suit_deck,6):
        best_hand6 = 8000 # Placeholders with the "worst" hand
        best_hand7 = 8000

        for five_cards in itertools.combinations(hand,5):
            best_hand6 = min(best_hand6, five_card_strength[five_cards])

        inverse_hand = [card for card in suit_deck if card not in hand] # 7 card combos
        for five_cards in itertools.combinations(inverse_hand,5):
            best_hand7 = min(best_hand7, five_card_strength[five_cards])

        flush67_dict[e._unique(hand)] = best_hand6
        flush67_dict[e._unique(inverse_hand)] = best_hand7

    pickle_dict('flush67_dict.pkl', flush67_dict)
    print("flush67 done")

    prime_factor_dict = {}

    for hand in itertools.combinations(d.cards,7):
        if _n_suit(hand) > 4:
            pass
        hand_key = e._matched_hand(hand)
        if hand_key not in prime_factor_dict:
            best_hand = 8000
            for fives_cards in itertools.combinations(hand,5):
                best_hand = min(best_hand, five_card_strength[fives_cards])
            prime_factor_dict[hand_key] = best_hand
        else:
            pass
    
    # print(len(prime_factor_dict)) ## 49205
    pickle_dict('prime_factor_dict.pkl', prime_factor_dict)
