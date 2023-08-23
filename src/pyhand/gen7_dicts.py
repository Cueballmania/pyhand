# To quickly calculate 7-card dictionaries, some observations are needed.
# 1. If the hand has 5 or more cards of the same suit, the best hand is
# either a flush or straight flush. Hence, we can use the 5-card table for
# 5-cards of the same suit. We need to generate a table that has 6 or 7 cards
# of the same suit.
# 2. If the hand has 4 or fewer cards of the same suit, then each hand can be
# classified by the product of the prime factors of cards.
# This still has millinos of combinations, so we need to reduce this number
# If we classify 7-card hands in the following way, we can reduce the number
# to the 49,205 unique non-flush combinations of faces.
# Further, to speed up generation of the tables, we first load the 5-card
# tables into memory and use them for quicker lookup.
if __name__ == "__main__":
    import deck as deck
    from itertools import chain, combinations, permutations
    from card import Card
    from typing import List
    from gen5_dicts import pickle_dict
    import evaluator as e
    import bit_calculator as bc

    d = deck.Deck()
    five_card_strength = {} # caching the hand value for use in 7-card validation
    for hand in combinations(d.cards,5):
        five_card_strength[hand] = e.evaluate_hand(hand)

    # Generate the flush67_dict
    # Observe that you only need to iterate through one suit's cards
    # finding all 6 card combos is equivalent to finding all 7 card combos
    # since 13C7 = 13C6
    flush67_dict = {}
    suit_deck = d.cards[0:13]

    for hand in combinations(suit_deck,6):
        best_hand6 = 8000 # Placeholders with the "worst" hand
        best_hand7 = 8000

        for five_cards in combinations(hand,5):
            best_hand6 = min(best_hand6, five_card_strength[five_cards])

        inverse_hand = [card for card in suit_deck if card not in hand] # 7 card combos
        for five_cards in combinations(inverse_hand,5):
            best_hand7 = min(best_hand7, five_card_strength[five_cards])

        flush67_dict[bc._unique(hand)] = best_hand6
        flush67_dict[bc._unique(inverse_hand)] = best_hand7

    pickle_dict('../data/flush67_dict.pkl', flush67_dict)
    print("flush67 done")

    matched7_hand_dict = {}

    # Create generators for all 7-card non-flush combinations
    quad_trips = ([pairs[0]]*4+[pairs[1]]*3 for pairs in permutations(suit_deck,2))
    quad_pair = ([triple[0]]*4+[triple[1]]*2 + [triple[2]] for triple in permutations(suit_deck,3))
    quad_nopair = ([card]*4+list(triple) for card in suit_deck for triple in combinations([card2 for card2 in suit_deck if card2 != card],3))

    trips_trips = ([pair[0]]*3+[pair[1]]*3+[card] for pair in combinations(suit_deck,2) for card in suit_deck if card not in pair)
    trips_2pair = ([card]*3+list(pair)*2 for card in suit_deck for pair in combinations([card2 for card2 in suit_deck if card2 != card],2))
    trips_pair = ([pair[0]]*3+[pair[1]]*2+list(pair2) for pair in permutations(suit_deck,2) for pair2 in combinations([card for card in suit_deck if card not in pair],2))
    trips_nopair = ([card]*3+list(quad) for card in suit_deck for quad in combinations([card2 for card2 in suit_deck if card2 != card],4))

    three_pair = (list(triple)*2 + [card] for triple in combinations(suit_deck,3) for card in suit_deck if card not in triple)
    two_pair = (list(pair)*2 + list(triple) for pair in combinations(suit_deck,2) for triple in combinations([card for card in suit_deck if card not in pair],3))
    one_pair = ([card]*2 + list(quint) for card in suit_deck for quint in combinations([card2 for card2 in suit_deck if card2 != card],5))
    no_pair = (list(sept) for sept in combinations(suit_deck,7))
    seven_perms = chain(quad_trips, quad_pair, quad_nopair, trips_trips,
                        trips_2pair, trips_pair, trips_nopair, three_pair,
                        two_pair, one_pair, no_pair)
    
    for hand in seven_perms:
        best_hand = 8000
        hand_key = bc._matched_hand(hand)
        for five_cards in combinations(hand,5):
            best_hand = min(best_hand, five_card_strength[five_cards])
        matched7_hand_dict[hand_key] = best_hand
    
    # print(len(prime_factor_dict)) ## 49205
    pickle_dict('../data/matched_7hand_dict.pkl', matched7_hand_dict)
    print*("matched hands 7 done")