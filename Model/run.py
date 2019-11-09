from Model.Version1 import Model
from Model.utils import *
import os

x_train, y_train, x_eval, y_eval = parse("../Game/Version0")
model = Model()
m = model.run(x_train, y_train, x_eval, y_eval)

generation = 1
version_folder_name = "Version1"
folder_name = "Generation" + str(generation)
try:
    os.mkdir(version_folder_name)
    os.mkdir("Version1/" + folder_name)

    m.save("Version1/" + folder_name + "/Model", include_optimizer=False)
    m.save_weights("Version1/" + folder_name + "/Weight")
except:
    print("Failed to make new directory")

