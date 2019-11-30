import random
import copy
from Game.Player import Player
from Game.Board import Board
from Game.Score import Score
from Game.Card import Card
from Game.calculator import Calculator
import Game.GoStopConstants as Const

class AI_random:
    @staticmethod
    def play(player: Player, board: Board, my_score: Score, opp_score: Score):
        for card in player._cards:
            m, _ = card.get()
            if len(board._board[m]) > 0:
                index = player._cards.index(card)
                return player.play(index)

        cards = copy.deepcopy(player._cards)
        cards.sort()
        recurrent_score = []
        my_jum = sum(Calculator.calculate(my_score))
        opp_jum = sum(Calculator.calculate(opp_score))
        appeared_card = []
        for t in Const.types:
            appeared_card.extend(my_score.get(t))
            appeared_card.extend(opp_score.get(t))
        appeared_card.sort()

        for i, card in enumerate(cards):
            score = 0
            if (i != 0 and cards[i]._month == cards[i-1]._month) or (i != len(cards)-1 and cards[i]._month == cards[i+1]._month):
                score += 100
            if card._month in [5, 7, 10, 12]:
                score += 1
            ms = copy.deepcopy(my_score)
            os = copy.deepcopy(opp_score)

            scored_cards = []
            for idx in range(4):
                scored_cards.append(Card(card._month, idx))
            os.add(cards)
            updated_opp_jum = sum(Calculator.calculate(os))

            if opp_jum < Const.go_score <= updated_opp_jum:
                score -= 1000
            elif updated_opp_jum > opp_jum:
                score -= 100

            potential_score = []
            for idx in range(4):
                potential_score.append(Card(card._month, idx))
            ms.add(cards)
            updated_my_jum = sum(Calculator.calculate(ms))

            if my_jum < updated_my_jum:
                score -= 10*(21-(2*len(player._cards)))

            temp = 30
            for appeared in appeared_card:
                m, _ = appeared.get()
                if m == card._month:
                    temp = 0
            score += temp
            recurrent_score.append(score)

        m = max(recurrent_score)
        selected = [i for i, v in enumerate(recurrent_score) if v == m]
        selected = selected[random.randint(0, len(selected)-1)]
        card = cards[selected]
        index = player.find_index(card._month, card._index)

        return player.play(index)

    @staticmethod
    def select(match):
        return 0

    @staticmethod
    def ask_go(is_last, opp_go):
        if is_last or opp_go:
            return False
        else:
            return True
