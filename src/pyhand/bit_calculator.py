# This module contains bit manipulation functions that are used for evaluating hands
# They are also used to generate lookup dictionaries in gen_dicts.py
from typing import List
from card import Card
from numpy import prod
from functools import reduce
from collections import Counter

# Checks if all of the cards are the same suit using bitwise AND
def _is_flush(cards: List[Card]) -> bool:
    flush = reduce(lambda x, y: x & y, [c.get_int_rep() for c in cards], 61440)
    if flush == 0:
        return False
    else:
        return True

# Checks to see if all of the card faces are unique from five cards
def _is_unique5(cards: List[Card]) -> bool:
    card_ranks = reduce(lambda x, y: x | y, [c.get_int_rep() for c in cards], 0) >> 16
    if card_ranks.bit_count() == 5:
        return True
    else:
        return False

# Creates a unique integer representation of the card faces
def _unique(cards: List[Card]) -> int:
    return reduce(lambda x, y: x | y, [c.get_int_rep() for c in cards], 0) >> 16

# Calculates the multiplication of the prime factors of the hand.
# This value is unique for all compariably sized hand faces
def _matched_hand(cards: List[Card]) -> int:
    return prod(list(map(lambda x: x.get_int_rep() & 255, cards)))

# Get the suit int from each card
def small_suit_calc(card: Card) -> int:
    return (card.get_int_rep() & 61440) >> 12

# Count the number of suits in the hand and return the greatest number
# Ties do not matter since the highest tie is 3/3/1 and a flush can only occur with 5 or more
def num_suit(cards: List[Card]) -> (int, int):
    suit_cnt = Counter([small_suit_calc(card) for card in cards])
    (small_suit, num) = suit_cnt.most_common(1)[0]
    return (small_suit << 12, num)

# Filter cards by a given suit int
def get_suited_cards(cards: List[Card], suit: int) -> List[Card]:
    return [card for card in cards if card.get_int_rep() & suit != 0]
