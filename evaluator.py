from typing import List
from numpy import prod
from functools import reduce
from card import Card
import pickle

flush_dict = pickle.load(open("flush_dict.pkl", "rb"))
unique5_dict = pickle.load(open("unique5_dict.pkl", "rb"))
matched_hand_dict = pickle.load(open("matched_hand_dict.pkl", "rb"))

def _is_flush(cards: List[Card]) -> bool:
    flush = reduce(lambda x, y: x & y, [c.get_int_rep() for c in cards], 61440)
    if flush == 0:
        return False
    else:
        return True

def _is_unique5(cards: List[Card]) -> bool:
    card_ranks = reduce(lambda x, y: x | y, [c.get_int_rep() for c in cards], 0) >> 16
    if card_ranks.bit_count() == 5:
        return True
    else:
        return False

def _unique5(cards: List[Card]) -> int:
    return reduce(lambda x, y: x | y, [c.get_int_rep() for c in cards], 0) >> 16

def _matched_hand(cards: List[Card]) -> int:
    return prod(list(map(lambda x: x.get_int_rep() & 255, cards)))

# This function takes in 5 cards and returns the integer representation of the hand's strength
# in order to determine the hand's strength, first check if all five cards are the same suit
# (1) if they are, then all 5 cards are unique, so calculate the binary representation of all five cards
# being in the hand and use that in the flush dictionary.
# (2) If they are not all the same suit, check if all five are unique. If they are, then it's either a 
# straight or a high card hand and use the unique5 dictionary.
# (3) If the five cards are not all the same suit nor are they all unique, use the matched hand dictionary
# which takes all of the prime representations and multiplies them to create a unique key for 
# 1P, 2P, 3K, 4K and FH hands.
def evaluate_hand(cards: List[Card]) -> int:
    if len(cards) != 5:
        return 0
    
    if _is_flush(cards):
        return flush_dict[_unique5(cards)]
    else:
        if _is_unique5(cards):
            return unique5_dict[_unique5(cards)]
        else:
            return matched_hand_dict[_matched_hand(cards)]

# Interpret evaluate_hand integer into human readable hand strength
def hand_strength(hand_eval: int) -> str:
    if hand_eval < 11:
        return "Straight Flush"
    elif hand_eval < 167:
        return "4 of a Kind"
    elif hand_eval < 323:
        return "Full House"
    elif hand_eval < 1600:
        return "Flush"
    elif hand_eval < 1610:
        return "Straight"
    elif hand_eval < 2468:
        return "3 of a Kind"
    elif hand_eval < 3326:
        return "2 Pair"
    elif hand_eval < 6186:
        return "1 Pair"
    else:
        return "High Card"

if __name__ == "__main__":
    import deck
    import itertools

    # {'Straight Flush': 40, '4 of a Kind': 624, 'Full House': 3744, 'Flush': 5108, 'Straight': 10200, '3 of a Kind': 54912, '2 Pair': 123552, '1 Pair': 1098240, 'High Card': 1302540}
    d = deck.Deck()
    five_card_strength = {}
    enumerated5 = {"Straight Flush": 0, 
                   "4 of a Kind": 0, 
                   "Full House": 0, 
                   "Flush": 0, 
                   "Straight": 0, 
                   "3 of a Kind": 0, 
                   "2 Pair": 0, 
                   "1 Pair": 0, 
                   "High Card": 0}
    for hand in itertools.combinations(d.cards,5):
        five_card_strength[hand] = evaluate_hand(hand)
        enumerated5[hand_strength(evaluate_hand(hand))] += 1
    
    print(enumerated5)

    # {'Straight Flush': 41584, '4 of a Kind': 224848, 'Full House': 3473184, 'Flush': 4047644, 'Straight': 6180020, '3 of a Kind': 6461620, '2 Pair': 31433400, '1 Pair': 58627800, 'High Card': 23294460}
    enumerated7 = {"Straight Flush": 0, 
                   "4 of a Kind": 0, 
                   "Full House": 0, 
                   "Flush": 0, 
                   "Straight": 0, 
                   "3 of a Kind": 0, 
                   "2 Pair": 0, 
                   "1 Pair": 0, 
                   "High Card": 0}
    for hand in itertools.combinations(d.cards,7):
        best_hand = 8000 # Placeholder with the "worst" hand
        for five_cards in itertools.combinations(hand,5):
            best_hand = min(best_hand, five_card_strength[five_cards])
        enumerated7[hand_strength(best_hand)] += 1
    
    print(enumerated7)