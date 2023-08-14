# This file contains constants used by the card class

# primes are used for each card's unique id
# 2 -> 2
# 3 -> 3
# 4 -> 5
# ...
# K -> 37
# A -> 41
_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
_cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T','J', 'Q', 'K', 'A']
prime_dict = {c : p for (c, p) in zip(_cards, _primes)}

# This lookup is for the int representation of suits
# Clubs = 0b1000 0000 0000 0000 = 32768
# Diamonds = 0b0100 0000 0000 0000
# Hearts = 0b0010 0000 0000 0000
# Spades = 0b0001 0000 0000 0000
suits_dict = {'C' : 32768,
              'D' : 16384,
              'H' : 8192,
              'S' : 4096}

# This lookup is for the int representation of ranks
# These are bitshifted to the left by 8 bits
rank_dict = {c : i for (i, c) in enumerate(_cards)}

