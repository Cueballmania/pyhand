import card

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
                self.cards.append(card.Card(face, suit))