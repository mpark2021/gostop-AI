import keras
from Model.BaseModel import BaseModel


class Model(BaseModel):
    def define_model(self) -> keras.Model:
        model = keras.Sequential(
            [
                keras.layers.Dense(32, input_dim=48 * 4, activation="sigmoid"),
                keras.layers.Dense(64, activation="sigmoid"),
                keras.layers.Dense(128, activation="sigmoid"),
                keras.layers.Dense(256, activation="sigmoid"),
                keras.layers.Dense(48, activation="sigmoid")
            ]
        )
        return model
