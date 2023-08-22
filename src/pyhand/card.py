# This code generates a class for a card object
import src.pyhand.card_constants as cc

class Card:
    def __init__(self, face: str, suit: str) -> None:
        self.face = face
        self.suit = suit
        self.int_rep = self._gen_int_rep()

    def _gen_int_rep(self) -> int:
        # uses the card_constants module to generate an integer representation of the card
        # the representation is a 32 bit integer in binary is
        # +--------+--------+--------+--------+
        # |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
        # +--------+--------+--------+--------+
        # p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
        # r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
        # cdhs = suit of card (bit turned on based on suit of card)
        # b = bit turned on depending on rank of card
        # x = unused 0
        return (1 << cc.rank_dict[self.face] + 16) + cc.suits_dict[self.suit] + (cc.rank_dict[self.face] << 8) + cc.prime_dict[self.face]

    def get_int_rep(self) -> int:
        return self.int_rep
    
    def get_bin_rep(self) -> str:
        return bin(self.int_rep)

    def get_bin_string(self) -> str:
        # returns the binary representation of the card as a string with spaces between each 4 bits
        reversed_str = str(self.get_bin_rep())[::-1]
        space_separated = ' '.join(reversed_str[i:i+4] for i in range(0, len(reversed_str), 4))
        return space_separated[::-1]

    def __repr__(self) -> str:
        return f'{self.face}{self.suit}'