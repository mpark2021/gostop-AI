from Card import Card
import GoStopConstants as Const

class Board:
    def __init__(self):
        self._board = {}
        for m in Const.cards:
            self._board[m] = []

    def __str__(self):
        s = "==========================================================\n"
        for m in self._board:
            for card in self._board[m]:
                s += str(card)
        s += "\n==========================================================\n"
        return s

    def put(self, card):
        m, t = card.get()
        self._board[m].append(card)

    def remove(self, cards): # controller 에 때라 interchangeable
        for card in cards:
            m, t = card.get()
            self._board[m].remove(card)

    def match(self, month):
        if len(self._board[month]) > 1:
            return self._board[month].copy()
        return[]


if __name__ =="__main__":
    from Library import Library
    library = Library()
    library.shuffle()
    board = Board()
    for i in range(7):
        board.put(library.draw())
    print(board)
