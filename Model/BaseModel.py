import keras
import Model.utils


class BaseModel:

    def define_model(self) -> keras.Model:
        raise NotImplementedError

    def run(self, x_train, y_train, x_eval, y_eval, batch_size = None, epochs=3000):
        model = self.define_model()
        model.summary()

        def select_accuracy(y_true, y_pred):

            return Model.utils.select_accuracy_internal(x_train, y_true, y_pred, keras.metrics.categorical_crossentropy)

        def select_accuracy_eval(y_true, y_pred):

            return Model.utils.select_accuracy_internal(x_eval, y_true, y_pred, keras.metrics.categorical_crossentropy)

        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy", select_accuracy])

        model.fit(x_train, y_train, batch_size=x_train.shape[0], epochs=epochs)

        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy", select_accuracy_eval])

        print(model.evaluate(x_eval, y_eval, batch_size=x_eval.shape[0]))

        return model
