import keras

model = keras.Sequential(
    [
        keras.layers.Dense(32, input_dim=48 * 4, activation="sigmoid"),
        keras.layers.Dense(64, activation="sigmoid"),
        keras.layers.Dense(48, activation="sigmoid")
    ]
)

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

