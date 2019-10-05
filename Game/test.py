from Card import Card
import GoStopConstants as Const
from Player import Player
from Library import Library
from Board import Board




if __name__ == "__main__":
    from Library import Library
    library = Library()
    library.shuffle()
    p1 = Player("A")
    p2 = Player("B")
    board = Board()

    for i in range (7):
        p1.draw(library.draw())
        p2.draw(library.draw())

    for i in range(6):
        board.put(library.draw())

    print(p1)
    print(p2)
    print(board)

    board.put(p1.play(0))

    print(p1)
    print(p2)
    print(board)