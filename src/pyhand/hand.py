from typing import List, Optional
from src.pyhand.card import Card
from src.pyhand.evaluator import evaluate_hand
import src.pyhand.deck as deck

def make_handlist(in_str: str) -> List[Card]:
    return [Card(in_str[c], in_str[c+1]) for c in range(0, len(in_str), 2)]

class Hand5:
    def __init__(self, cards: Optional[List[Card]]=None) -> None:
        if cards is None:
            self._build_hand()
        else: 
            if len(cards) != 5:
                self._build_hand()
            else:
                self.cards = cards
        self.hand_value =  evaluate_hand(self.cards)

    def _build_hand(self) -> None:
        d = deck.Deck()
        d.shuffle()
        self.cards = d.cards[0:5]

    def get_hand(self) -> List[Card]:
        return self.cards

    def __repr__(self) -> str:
        return " ".join([str(c) for c in self.cards])