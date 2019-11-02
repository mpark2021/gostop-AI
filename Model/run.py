from Model.Ver1 import Model_Version1
from Model.utils import *
import os

x_train, y_train, x_eval, y_eval = parse("../Game/version1")
model = Model_Version1()
m = model.run(x_train, y_train, x_eval, y_eval)

m.save("Version1/Model", include_optimizer=False)
m.save_weights("Version1/Weight")