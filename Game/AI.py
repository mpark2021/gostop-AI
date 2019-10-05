import random
from Player import Player
from Board import Board

class AI:
    @staticmethod
    def play(player: Player, board: Board):
        for card in player._cards:
            m, _ = card.get()
            if len(board._board[m]) > 0:
                index = player._cards.index(card)
                return player.play(index)
        return player.play(0)

    @staticmethod
    def select(match):
        return 0

    @staticmethod
    def ask_go(is_last, opp_go):
        if is_last or opp_go:
            return False
        else:
            return True
