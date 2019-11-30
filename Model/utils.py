import numpy as np
import gzip
import tensorflow as tf

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

def select_accuracy_internal(x, y, y_pred, accuracy):
    x_hand = np.split(x, [48, ], 1)[0]
    x_hand = tf.convert_to_tensor(x_hand, dtype=tf.float32)
    y_pred = tf.convert_to_tensor(y_pred, dtype=tf.float32)
    y_pred_hand = tf.math.multiply(x_hand, y_pred)
    return accuracy(y, y_pred_hand)



if __name__ == "__main__":
    x, y, x_eval, y_eval = parse("../Game/version1")
    x_acc_test = x[:10]
    y_acc_test = y[:10]
    y_acc_test_pred = np.random.random((10, 48))
    import keras
    import tensorflow as tf
    acc = select_accuracy_internal(x_acc_test, y_acc_test, y_acc_test_pred, keras.metrics.accuracy)
    sess = tf.Session()
    value = sess.run(acc)
    print(value)
