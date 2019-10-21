import numpy as np
import gzip

def parse(dir):
    x = []
    y = []

    with gzip.open(dir+"/x_game.txt", "rb") as f:
        while True:
            line = f.readline().decode()
            if not line:
                break
            line = line[:-1]
            x_m = list(map(int, list(line)))
            x.append(x_m)

    with gzip.open(dir+"/y_game.txt", "r") as f:
        while True:
            line = f.readline().decode()
            if not line:
                break
            line = line[:-1]
            y_m = [int(y == int(line)) for y in range(48)]
            y.append(y_m)


    divider = int(len(x) * 0.7)
    x_train = np.asarray(x[:divider])
    x_eval = np.asarray(x[divider:])
    y_train = np.asarray(y[:divider])
    y_eval = np.asarray(y[divider:])

    return x_train, y_train, x_eval, y_eval


if __name__ == "__main__":
    parse("../Game/version1")
