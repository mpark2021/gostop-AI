import keras


def forward(model_path, weights_path, data):
    with open(model_path, "r") as f:
        json = f.read()
        model = keras.models.model_from_json(json)
        model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
        model.load_weights(weights_path)
        return model(data)