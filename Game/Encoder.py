import GoStopConstants as Const

class Encoder:
    @staticmethod
    def encode(player, board, my_score, opp_score):
        result = []
        for i in range(4):
            for m in Const.cards:
                for t in Const.cards[m]:
                    result.append(0)

        diff = 48

        for card in player._cards:
            m, i = card.get_raw()
            result[(m-1) * 4 + i] = 1

        for m in board._board:
            for card in board._board[m]:
                _, i = card.get_raw()
                result[(m-1) * 4 + i + diff] = 1

        for t in my_score._cards:
            for card in my_score._cards[t]:
                m, i = card.get_raw()
                result[(m-1) * 4 + i + diff * 2] = 1

        for t in opp_score._cards:
            for card in opp_score._cards[t]:
                m, i = card.get_raw()
                result[(m-1) * 4 + i + diff * 3] = 1

        return result

    @staticmethod
    def to_string(encoded):
        s = ""
        for data in encoded:
            s += str(data)
        s += "\n"
        return s