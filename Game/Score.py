import Game.GoStopConstants as Const


class Score:
    def __init__(self):
        self._cards = {}
        self._gwang_score = 0
        self._ddi_score = 0
        self._pi_score = 0
        self._gut_score = 0
        self._total_score = 0
        self._go = 0
        self._nine_gut = None
        for t in Const.types:
            self._cards[t] = []

    def __str__(self):
        s = ""
        for t in self._cards:
            for card in self._cards[t]:
                s += str(card)
            s += "/"
        s += "%d점" % self._total_score
        return s

    def add(self, cards):
        for card in cards:
            m, t = card.get()
            if card not in self._cards[t]:
                self._cards[t].append(card)
                if m == 8 and t == 2:
                    self._nine_gut = card

    def get(self, t):
        return self._cards[t].copy()

    def go(self):
        self._go += 1

    def get_go_count(self):
        return self._go

    def get_nine(self):
        return self._nine_gut

    def set_score(self, gwang, ddi, gut, pi, value):
        self._gwang_score = gwang
        self._ddi_score = ddi
        self._gut_score = gut
        self._pi_score = pi
        self._total_score = value

    def get_score(self):
        return self._gwang_score, self._ddi_score, self._gut_score, self._pi_score, self._total_score
