import GoStopConstants as Const
from Score import Score
from Player import Player

class Calculator:
    @staticmethod
    def calculate(scored: Score) -> (int, int, int, int):
        # 1. 광
        gwang_score = Calculator._calc_gwang(scored.get(4))
        # 2. 띠
        ddi_score = Calculator._calc_ddi((scored.get(3)))
        # 3. others
        gut = scored.get(2)
        ssang = scored.get(1)
        pi = scored.get(0)
        nine_gut = scored.get_nine()
        if nine_gut is None:
            gut_score = Calculator._calc_gut(gut)
            pi_score = Calculator._calc_pi(pi, ssang)
        else:

            score_nine_gut = [Calculator._calc_gut(gut), Calculator._calc_pi(pi, ssang)]
            gut.remove(nine_gut)
            ssang.append(nine_gut)
            score_nine_ssang = [Calculator._calc_gut(gut), Calculator._calc_pi(pi, ssang)]
            if sum(score_nine_gut) > sum(score_nine_ssang):
                gut_score = score_nine_gut[0]
                pi_score = score_nine_gut[1]
            else:
                gut_score = score_nine_ssang[0]
                pi_score = score_nine_ssang[1]

        return gwang_score, ddi_score, gut_score, pi_score

    @staticmethod
    def calculate_go(winner: Score):
        add = 0
        mult = 1
        go = winner.get_go_count()
        if go < 3:
            add += go
        else:
            add += 2
            mult *= 2**(go-2)

        return add, mult

    @staticmethod
    def multiplier(winner: Score, loser: Score):
        mult = 1
        if loser.get_go_count() > 0:
            mult *= 2

        winner_score = winner.get_score()
        if loser.get_nine() is not None:
            loser_nine = 2
        else:
            loser_nine = 0

        if winner_score[3] > 0 and (len(loser.get(0)) + 2*len(loser.get(1)) + loser_nine) < 7:
            mult *= 2

        if winner_score[0] > 0 and (len(loser.get(4))) == 0:
            mult *= 2

        return mult

    @staticmethod
    def _calc_gwang(gwang):
        score = 0
        if len(gwang) == 5:
            score += 15
        elif len(gwang) == 4:
            score += 4
        elif len(gwang) == 3:
            score += 3
            for card in gwang:
                m, _ = card.get()
                if m == 12:
                    score -= 1
        return score

    @staticmethod
    def _calc_ddi(ddi):
        score = 0
        blue = 0
        red = 0
        cho = 0
        for card in ddi:
            m, _ = card.get()
            if m in Const.blue:
                blue += 1
            elif m in Const.red:
                red += 1
            elif m in Const.cho:
                cho += 1

        if blue > 3:
            score += 3
        if red > 3:
            score += 3
        if cho > 3:
            score += 3

        if len(ddi) > 4:
            score += len(ddi) - 4

        return score

    @staticmethod
    def _calc_gut(gut):
        score = 0
        godori = 0
        for card in gut:
            m, _ = card.get()
            if m in Const.godori:
                godori += 1
        if godori > 3:
            score += 5
        if len(gut) > 4:
            score += len(gut) - 4

        return score

    @staticmethod
    def _calc_pi(pi, ssang):
        score = 0
        if len(pi) + 2*len(ssang) > 9:
            score += len(pi) + 2*len(ssang) - 9

        return score