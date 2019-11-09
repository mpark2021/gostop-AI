from Game.Library import Library
from Game.Board import Board
from Game.Player import Player
from Game.Card import Card
from Game.Score import Score
from Game.AI_random import AI_random
import random
from Game.Encoder import Encoder
from Game.calculator import Calculator
import Game.GoStopConstants as Const
import gzip


class Game:
    def __init__(self, is_user=True):
        self._board_record = []
        self._played_record = []

        self._is_user = is_user
        self._x_filename = "x_game.txt"
        self._y_filename = "y_game.txt"

        self._reset()

    def _reset(self):
        self._library = Library()
        self._board = Board()
        self._player1 = Player("A")
        self._player2 = Player("B")
        self._players = [self._player1, self._player2]
        self._scores = [Score(), Score()]

        self._turn_side = random.randint(0, 1)  # if 0, player 1 starts first
        if self._is_user:
            if self._turn_side == 0:
                print("Player First")
            else:
                print("Player Second")
        self._library.shuffle()
        for i in range(10):
            self._player1.draw(self._library.draw())
            self._player2.draw(self._library.draw())
        for i in range(8):
            self._board.put(self._library.draw())

        if self._is_user:
            print(self)

    def __str__(self):
        s = ""
        s += str(self._player2) + "\n"
        s += str(self._scores[1]) + "\n"
        s += str(self._board) + "\n"
        s += str(self._scores[0]) + "\n"
        s += str(self._player1) + "\n"
        return s

    def run_with_encode(self, num_iter):
        self._board_record = []
        self._played_record = []

        for i in range(num_iter):
            self._reset()
            self.run()

        with gzip.open(self._x_filename, "wb") as f:
            for line in self._board_record:
                f.write(line.encode())

        with gzip.open(self._y_filename, "wb") as f:
            for played in self._played_record:
                f.write((str(played) + "\n").encode())


    def run(self):

        record = [[], []]
        played = [[], []]

        is_last = False
        winner = None

        while len(self._library) > 0:
            encoded = Encoder.encode(self._players[1], self._board, self._scores[1], self._scores[0])
            # encoded.insert(0, self._turn_side) (lstm때 쓸 수 도 있음)

            played_card = None
            if self._players[self._turn_side].get_hand_count() > 0:
                if self._turn_side == 0 and self._is_user:
                    played_card = self.user_input()
                else:
                    played_card = AI_random.play(self._players[self._turn_side], self._board)
            drew = self._library.draw()

            if played_card is not None:
                self._board.put(played_card)
                record[self._turn_side].append(Encoder.to_string(encoded))
                played[self._turn_side].append(Encoder.encode_played(played_card))
            self._board.put(drew)

            self.update(played_card, drew)

            total_score, prev_total = self._calculate_score()

            if self._is_user:
                print(self)

            if not self._check_go(total_score, prev_total):
                winner = self._turn_side
                break

            self._change_player()
        if self._is_user:
            self._print_winner(winner)
        if winner is not None:
            self._board_record.extend(record[winner])
            self._played_record.extend(played[winner])

    def _calculate_score(self):
        gwang, ddi, gut, pi = Calculator.calculate(self._scores[self._turn_side])
        total_score = gwang + ddi + gut + pi
        _, _, _, _, prev_total = self._scores[self._turn_side].get_score()
        self._scores[self._turn_side].set_score(gwang, ddi, gut, pi, total_score)
        return total_score, prev_total

    def _check_go(self, curr_score, prev_score):
        if curr_score > Const.go_score and curr_score > prev_score:
            answer = self.ask_go()
            if answer:
                self._scores[self._turn_side].go()
                return True
            else:
                return False
        else:
            return True

    def _get_opp(self):
        return(self._turn_side + 1) % 2

    def _change_player(self):
        self._turn_side = self._get_opp()

    def _print_winner(self, winner):
        if winner is not None:
            _, _, _, _, score = self._scores[winner].get_score()
            go_add, go_mult = Calculator.calculate_go(self._scores[winner])
            score = (score + go_add) * go_mult
            multiplier = Calculator.multiplier(self._scores[winner], self._scores[(winner + 1) % 2])
            score = score * multiplier
            print("Winner is player %d! Score: %d" % (winner + 1, score))
        else:
            print("No Winner")

    def ask_go(self) -> bool:
        if self._turn_side == 0 and self._is_user:
            while True:
                answer = input("go or stop?")
                if answer == "go":
                    return True
                elif answer == "stop":
                    return False
        else:
            is_last = len(self._library) <= 2
            opp_go = self._scores[self._get_opp()].get_go_count() > 0
            return AI_random.ask_go(is_last, opp_go)

    def user_input(self) -> Card:
        try:
            selected = int(input("Select card: "))
            card = self._player1.play(selected)
            if card is None:
                print("Input a proper number")
                return self.user_input()
            else:
                return card

        except ValueError:
            print("Input a number")
            return self.user_input()

    def update(self, played, drew):
        if played is None:
            played_m = -1
        else:
            played_m, _ = played.get()
        drew_m, _ = drew.get()

        scored = []
        if played_m == drew_m:
            match = self._board.match(played_m)
            if len(match) == 4 or len(match) == 2:
                scored.extend(match)
        else:
            for c in (played, drew):
                if c is None:
                    continue

                month, _ = c.get()
                if month == -1:
                    continue

                match = self._board.match(month)
                if len(match) == 4 or len(match) == 2:
                    scored.extend(match)
                elif len(match) == 3:
                    scored.append(c)
                    match.remove(c)
                    for card in match:
                        if self._is_user:
                            print(card)
                    if self._turn_side == 0 and self._is_user:
                        selected = int(input("Choose one card: "))
                    else:
                        selected = AI_random.select(match)
                    scored.append(match[selected])

        self._scores[self._turn_side].add(scored)
        self._board.remove(scored)


if __name__ == "__main__":
    import os
    version = "Version1"
    generation = "Generation0"
    try:
        if not os.path.exists(version):
            os.makedirs(version)
        os.chdir(version)

        if not os.path.exists(generation):
            os.makedirs(generation)
        os.chdir(generation)

        game = Game(False)
        game.run_with_encode(1000)

    except OSError:
        print("Failed to create directory")
