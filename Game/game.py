from Library import Library
from Board import Board
from Player import Player
from Card import Card
from Score import Score
from AI import AI
import random
from Encoder import Encoder
from calculator import Calculator
import GoStopConstants as Const


class Game:
    def __init__(self, p1_name, p2_name, number=1, is_user=True):
        self._library = Library()
        self._board = Board()
        self._is_user = is_user
        self._encoder = Encoder()
        self._filename = "game"+str(number)+".txt"

        self._player1 = Player(p1_name)
        self._player2 = Player(p2_name)
        self._players = [self._player1, self._player2]
        self._scores = [Score(), Score()]

        self._turn_side = random.randint(0,1) # if 0, player 1 starts first

        if self._turn_side == 0:
            print("Player First")
        else:
            print("Player Second")
        self._library.shuffle()
        for i in range(7):
            self._player1.draw(self._library.draw())
            self._player2.draw(self._library.draw())
        for i in range(6):
            self._board.put(self._library.draw())
        print(self)

    def __str__(self):
        s = ""
        s += str(self._player2) + "\n"
        s += str(self._scores[1]) + "\n"
        s += str(self._board) + "\n"
        s += str(self._scores[0]) + "\n"
        s += str(self._player1) + "\n"
        return s

    def run(self):
        with open(self._filename, "w") as f:

            is_last = False
            winner = None

            while len(self._library) > 0:
                encoded = Encoder.encode(self._players[1], self._board, self._scores[1], self._scores[0])
                encoded.insert(0, self._turn_side)
                f.write(Encoder.to_string(encoded))

                played_card = None
                if self._players[self._turn_side].get_hand_count() > 0:
                    if self._turn_side == 0 and self._is_user:
                        played_card = self.user_input()
                    else:
                        played_card = AI.play(self._players[self._turn_side], self._board)
                drew = self._library.draw()

                if played_card is not None:
                    self._board.put(played_card)
                self._board.put(drew)

                self.update(played_card, drew)

                total_score, prev_total = self._calculate_score()

                print(self)

                if not self._check_go(total_score, prev_total):
                    winner = self._turn_side
                    break

                self._change_player()

            encoded = Encoder.encode(self._players[1], self._board, self._scores[1], self._scores[0])
            encoded.insert(0, self._turn_side)
            f.write(Encoder.to_string(encoded))

            self._print_winner(winner)
            f.close()

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
            return AI.ask_go(is_last, opp_go)

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
                        print(card)
                    if self._turn_side == 0 and self._is_user:
                        selected = int(input("Choose one card: "))
                    else:
                        selected = AI.select(match)
                    scored.append(match[selected])

        self._scores[self._turn_side].add(scored)
        self._board.remove(scored)


if __name__ == "__main__":
    import os
    version = "version1"
    try:
        if not os.path.exists("version1"):
            os.makedirs(version)
        os.chdir(version)

        for i in range(10):
            game = Game("Player A", "Player B", i+1, False)
            game.run()

    except OSError:
        print("Failed to create directory")
