from Model.Version1 import Model
from Model.utils import *
import os

x_train, y_train, x_eval, y_eval = parse("../Game/version1")
model = Model()
m = model.run(x_train, y_train, x_eval, y_eval)

m.save("Version1/Model", include_optimizer=False)
m.save_weights("Version1/Weight")