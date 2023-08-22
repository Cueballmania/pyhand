# The strategy to create the dictionaries for the 7 card evaluator is to 
# first run the 5 card evaluator to create a dictionary of all 5 card hands
# then iterate all of the 7 card hands to map them to the best 5 card hand they can make
# each of these are stored in the correct place
import src.pyhand.deck as deck
import itertools
import collections
import pickle
from src.pyhand.card import Card
from typing import List
import src.pyhand.evaluator as e

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
        else:
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

# 7 card permutations. Need to format and test.
# from itertools import chain, combinations, permutations
# value_deck = suit_deck
# quad_trips = ([pairs[0]]*4+[pairs[1]]*3 for pairs in permutations(value_deck,2))
# quad_pair = ([triple[0]]*4+[triple[1]]*2 + [triple[2]] for triple in permutations(value_deck,3))
# quad_nopair = ([card]*4+list(triple) for card in value_deck for triple in combinations([card2 for card2 in value_deck if card2 != card],3))

# trips_trips = ([pair[0]]*3+[pair[1]]*3+[card] for pair in combinations(value_deck,2) for card in value_deck if card not in pair)
# trips_2pair = ([card]*3+list(pair)*2 for card in value_deck for pair in combinations([card2 for card2 in value_deck if card2 != card],2))
# trips_pair = ([pair[0]]*3+[pair[1]]*2+list(pair2) for pair in permutations(value_deck,2) for pair2 in combinations([card for card in value_deck if card not in pair],2))
# trips_nopair = ([card]*3+list(quad) for card in value_deck for quad in combinations([card2 for card2 in value_deck if card2 != card],4))

# three_pair = (list(triple)*2 + [card] for triple in combinations(value_deck,3) for card in value_deck if card not in triple)
# two_pair = (list(pair)*2 + list(triple) for pair in combinations(value_deck,2) for triple in combinations([card for card in value_deck if card not in pair],3))
# one_pair = ([card]*2 + list(quint) for card in value_deck for quint in combinations([card2 for card2 in value_deck if card2 != card],5))
# no_pair = (list(sept) for sept in combinations(value_deck,7))
# seven_perms = chain(quad_trips, quad_pair, quad_nopair, trips_trips,
#                     trips_2pair, trips_pair, trips_nopair, three_pair,
#                     two_pair, one_pair, no_pair)