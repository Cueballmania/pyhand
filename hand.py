from typing import List, Optional
from card import Card
from evaluator import evaluate_hand
import deck

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