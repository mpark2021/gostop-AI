from Game.AI_random import AI_random
from Game.Encoder import Encoder
import keras
import numpy as np
import tensorflow as tf

class AI:
    def __init__(self, version, generation):
        self.use_random = generation == 0
        if not self.use_random:
            self.model = self._load_model(version, generation)

    def play(self, player, board, my_score, opp_score):
        if self.use_random:
            return AI_random.play(player, board)
        else:
            encoded = Encoder.encode(player, board, my_score, opp_score)
            data = np.asarray([encoded])
            x = tf.convert_to_tensor(data, dtype=tf.float32)
            result = self.model(x)
            value = keras.backend.eval(result)
            value = value * np.split(data, [48,], 1)[0]

            card_id = np.argmax(value)
            m = card_id // 4 + 1
            i = card_id % 4

            return player.play(player.find_index(m, i))

    def select(self, match):
        return AI_random.select(match)

    def ask_go(self, is_last, opp_go):
        return AI_random.ask_go(is_last, opp_go)

    def _load_model(self, version, generation):
        path = "../../../Model/Version%d/Generation%d" % (version, generation)
        model_path = path + "/Model"
        weights_path = path + "/Weights"

        model = keras.models.load_model(model_path)
        model.compile(optimizer="adam",
                      loss="sparse_categorical_crossentropy",
                      metrics=["accuracy"])
        model.load_weights(weights_path)
        return model