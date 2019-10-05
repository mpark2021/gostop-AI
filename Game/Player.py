from Game.Score import Score


class Player:
    def __init__(self, name):
        self._name = name
        self._cards = []

    def __str__(self):
        s = "%s\n" % self._name
        for card in self._cards:
            s += str(card) + " "
        return s

    def get_hand_count(self):
        return len(self._cards)

    def draw(self, card):
        self._cards.append(card)

    def play(self, index):
        if not 0 <= index < len(self._cards):
            return None

        card = self._cards[index]
        self._cards.remove(card)
        return card


if __name__ == "__main__":
    from Game.Library import Library
    library = Library()
    library.shuffle()
    player = Player("A")
    player.draw(library.draw())
    player.draw(library.draw())
    player.draw(library.draw())
    print(player)
    print(player.play(0))
    print(player)

