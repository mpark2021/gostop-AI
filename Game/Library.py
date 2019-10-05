# Shuffle (Use Fisher-Yates Shuffle)
import random
import GoStopConstants as Const
from Card import Card


class Library:
    def __init__(self):
        self._cards = []
        for m in Const.cards:
            for i in range(len(Const.cards[m])):
                self._cards.append(Card(m, i))

    def __str__(self):
        s = ""
        counter = 0
        for c in self._cards:
            s += str(c) + " "
            counter += 1
            if counter > 3:
                counter = 0
                s += "\n"
        return s

    def __len__(self):
        return len(self._cards)

    def shuffle(self):
        n = len(self._cards)
        for i in range(len(self._cards)-1):
            j = random.randint(0, n-i-1) + i
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]

    def draw(self) -> Card:
        card = self._cards[-1]
        self._cards.remove(card)
        return card


if __name__ == "__main__":
    library = Library()
    library.shuffle()
    library.draw()
    print(library)





