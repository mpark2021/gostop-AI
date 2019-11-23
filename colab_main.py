import os
import sys

sys.path.insert(0, '/content/gdrive/My Drive/Colab Notebooks/')

def game_main(version, generation, num_iter=1000):
    from Game.game import Game

    version_path = "Game/Version%d" % version
    generation_path = version_path + "/Generation%d" % generation

    try:
        if not os.path.exists(version_path):
            os.makedirs(version_path)

        if not os.path.exists(generation_path):
            os.makedirs(generation_path)

    except OSError:
        print("Failed to create directory")
        exit(-1)

    game = Game(False, version, generation, filepath=generation_path)
    game.run_with_encode(num_iter)


def model_main(version, generation, epoch):
    from Model.Version1 import Model
    import Model.utils as utils
    x_train, y_train, x_eval, y_eval = utils.parse("Game/Version%d/Generation%d" % (version, generation))
    model = Model()
    m = model.run(x_train, y_train, x_eval, y_eval, epochs=epoch)

    version_folder_name = "Version" + str(version)
    folder_name = "Generation" + str(generation + 1)
    try:
        if not os.path.exists(version_folder_name):
            os.mkdir(version_folder_name)
        if not os.path.exists(version_folder_name + "/" + folder_name):
            os.mkdir(version_folder_name + "/" + folder_name)

        m.save(version_folder_name + "/" + folder_name + "/Model", include_optimizer=False)
        m.save_weights(version_folder_name + "/" + folder_name + "/Weights")
    except OSError:
        print("Failed to make new directory")


def main():
    argc = len(sys.argv)
    if argc < 4:
        print("Usage")
        print("[G|Game|g|game] version generation num_iter")
        print("[M|Model|m|model] version generation epoch=1000")
        return

    version = int(sys.argv[2])
    generation = int(sys.argv[3])

    if sys.argv[1] in ["G", "Game", "g", "game"]:
        if len(sys.argv) == 5:
            num_iter = int(sys.argv[4])
        else:
            num_iter = 1000
        game_main(version, generation, num_iter)

    elif sys.argv[1] in ["M", "Model", "m", "model"]:
        if len(sys.argv) == 5:
            epoch = int(sys.argv[4])
        else:
            epoch = 1000
        model_main(version, generation, epoch)
    else:
        print("Unknown command: " + sys.argv[1])


if __name__ =="__main__":
    main()