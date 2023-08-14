# This code generates a class for a card object
import card_constants as cc

class Card:
    def __init__(self, face: str, suit: str, value: int) -> None:
        self.face = face
        self.suit = suit
        self.value = value
        self.int_rep = self._gen_int_rep()

    def _gen_int_rep(self) -> int:
        return (1 << cc.rank_dict[self.face] + 16) + cc.suits_dict[self.suit] + (cc.rank_dict[self.face] << 8) + cc.prime_dict[self.face]

    def get_int_rep(self) -> int:
        return self.int_rep
    
    def get_bin_rep(self) -> int:
        return bin(self.int_rep)