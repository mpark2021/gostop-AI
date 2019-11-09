from Model.Version1 import Model
from Model.utils import *
import os

x_train, y_train, x_eval, y_eval = parse("../Game/Version1/Generation0")
model = Model()
m = model.run(x_train, y_train, x_eval, y_eval)

generation = 1
version_folder_name = "Version1"
folder_name = "Generation" + str(generation)
try:
    if not os.path.exists(version_folder_name):
        os.mkdir(version_folder_name)
    if not os.path.exists(version_folder_name + "/" + folder_name):
        os.mkdir(version_folder_name + "/" + folder_name)

    m.save(version_folder_name + "/" + folder_name + "/Model", include_optimizer=False)
    m.save_weights(version_folder_name + "/" + folder_name + "/Weights")
except OSError:
    print("Failed to make new directory")

