from src.pyhand.card import Card
from typing import List
import random

class Deck:
    def __init__(self) -> None:
        self.cards = []
        self.build()

    def build(self) -> None:
        suits = ['c', 'd', 'h', 's']
        faces = ['2', '3', '4', '5', '6', '7',
                 '8', '9', 'T', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for face in faces:
                self.cards.append(Card(face, suit))

    def shuffle(self, seed=None) -> None:
        # very basic shuffle

        if seed:
            random.seed(seed)
        random.shuffle(self.cards)