import keras

def forward(model_path, weights_path, data):
        model = keras.models.load_model(model_path)
        model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
        model.load_weights(weights_path)
        return model(data)


if __name__ =="__main__":
    import numpy as np
    import tensorflow as tf
    data = np.random.random((1, 48*4))
    data = data.round()
    x = tf.convert_to_tensor(data, dtype=tf.float32)
    y = forward("Version1/Model", "Version1/Weights", x)
    print(y)
    value = keras.backend.eval(y)
    print(value * np.split(data, [48,], 1)[0])
