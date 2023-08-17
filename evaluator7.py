# Create all of the 7 card hand evaluations
# Procedure:
# 1. Count the number of each suit in the 7-card hand
# 2a. If the number of any suit is fewer than 5, then the hand does a prime-factorization lookup
# 2b. If the number of any suit is 5 or more, the only possible best hand is a flush or straight flush
# 2b1. If the number of that suit is 5, use the 5 card flush lookup
# 2b2. If the number in that suit is 6 or 7 cards use the computed 6,7-card flush combined lookup

import collections
import itertools
from numpy import prod
import pickle
from typing import List
from functools import reduce
from card import Card

flush5_dict = pickle.load(open("flush_dict.pkl", "rb"))
flush67_dict = pickle.load(open("flush67_dict.pkl", "rb"))
prime_factor_dict = pickle.load(open("prime_factor_dict.pkl", "rb"))

# Get the suit string from each card
def small_suit_calc(card: Card) -> int:
    return (card.get_int_rep() & 61440) >> 12

# Count the number of suits in the hand and return the greatest
# Ties do not matter since the highest tie is 3/3/1 and a flush can only occur with 5 or more
def num_suit(cards: List[Card]) -> (int, int):
    suit_cnt = collections.Counter([small_suit_calc(card) for card in cards])
    (small_suit, num) = suit_cnt.most_common(1)[0]
    return (small_suit << 12, num)

# Get the unique binary indicators of cards in a suit
def _unique(cards: List[Card]) -> int:
    return reduce(lambda x, y: x | y, [c.get_int_rep() for c in cards], 0) >> 16

# Filter cards by a given suit int
def get_suited_cards(cards: List[Card], suit: int) -> List[Card]:
    return [card for card in cards if card.get_int_rep() & suit != 0]

# Use the prime numbers to get a product for unique lookup
def prime_factorization_lookup(cards: List[Card]) -> int:
    return prod(list(map(lambda x: x.get_int_rep() & 255, cards)))

# Given five cards of a suit, look up using the 5-card flush table
def flush5_lookup(cards: List[Card]) -> int:
    return flush5_dict[_unique(cards)]

# Use the 6,7-card flush table
def flush67_lookup(cards: List[Card]) -> int:
    return flush67_dict[_unique(cards)]

# Evaluate a 7-card hand
def evaluate7_hand(cards: List[Card]) -> int:
    (high_suit, num) = num_suit(cards)
    if num < 5:
        return prime_factor_dict[prime_factorization_lookup(cards)]
    elif num == 5:
        suited_cards = get_suited_cards(cards, high_suit)
        return flush5_lookup(suited_cards)
    else:
        suited_cards = get_suited_cards(cards, high_suit)
        return flush67_lookup(suited_cards)