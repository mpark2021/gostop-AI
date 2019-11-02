from Model.Ver1 import model
from Model.utils import *
import os

model.summary()
x_train, y_train, x_eval, y_eval = parse("../Game/version1")
print(x_train)
print(y_eval)
model.fit(x_train, y_train, epochs=100)

result = model.evaluate(x_eval, y_eval)
print(result)


if not os.path.exists("Version1"):
    os.mkdir("Version1")

model.save("Version1/model")
model.save_weights("Version1/weights")