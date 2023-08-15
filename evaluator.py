from typing import List
from numpy import prod
import functools
from card import Card
import hand

def _is_flush(cards: List[Card]) -> bool:
    flush = functools.reduce(lambda x, y: x & y, [c.get_int_rep() for c in cards], 61440)
    if flush == 0:
        return False
    else:
        return True

def _is_unique5(cards: List[Card]) -> bool:
    card_ranks = functools.reduce(lambda x, y: x | y, [c.get_int_rep() for c in cards], 0) >> 16
    if card_ranks.bit_count() == 5:
        return True
    else:
        return False

def _unique5(cards: List[Card]) -> int:
    return functools.reduce(lambda x, y: x | y, [c.get_int_rep() for c in cards], 0) >> 16

def _matched_hand(cards: List[Card]) -> int:
    return prod(list(map(lambda x: x.get_int_rep() & 255, cards)))

# This function takes in 5 cards and returns the integer representation of the hand's strength
def evaluate_hand(cards: List[Card]) -> int:
    if len(cards) != 5:
        return 0
    
    if _is_flush(cards):
        print("straight flush or flush")
        return _unique5(cards)
    else:
        if _is_unique5(cards):
            print("stright or high card")
            return _unique5(cards)
        else:
            print("pair, two pair, three of a kind, or full house")
            return _matched_hand(cards)