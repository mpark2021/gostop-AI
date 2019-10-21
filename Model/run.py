from Model.Ver1 import model
from Model.utils import *

model.summary()
x_train, y_train, x_eval, y_eval = parse("../Game/version1")
model.fit(x_train, y_train, epochs=100)

result = model.evaluate(x_eval, y_eval)
print(result)