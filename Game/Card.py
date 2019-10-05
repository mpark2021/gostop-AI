import Game.GoStopConstants as Const

class Card:
    def __init__(self, month, index):
        self._month = month
        self._index = index
        self._type = Const.cards[self._month][index]

    def __str__(self):
        return "[%d월, %s]" % (self._month, Const.types[self._type])

    def get(self):
        t = (self._month, self._type)  # tuple!!!
        return t

    def get_raw(self):
        index = (self._month, self._index)
        return index

if __name__ == "__main__":
    s = ""
    for m in range(1, 13):
        d = Const.cards[m]
        for t in d:
            s += str(Card(m, t)) + " "
        s += "\n"
    print(s)



