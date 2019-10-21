import numpy as np


def parse(dir):
    x = []
    y = []

    with open(dir+"/x_game.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line[:-1]
            x_m = list(map(int, list(line)))
            x.append(x_m)

    with open(dir+"/y_game.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line[:-1]
            y_m = [int(y == int(line)) for y in range(48)]
            y.append(y_m)

    x = np.asarray(x)
    y = np.asarray(y)

    return x, y


if __name__ == "__main__":
    parse("../Game/version1")
