import os
import sys

sys.path.insert(0, '/content/gdrive/My Drive/Colab Notebooks/')


def main():
    argc = len(sys.argv)
    if argc < 4:
        print("Usage")
        print("[G|Game|g|game] version generation num_iter")
        print("[M|Mode|m|mode] version generation epoch=1000")
        return

    version = int(sys.argv[2])
    generation = int(sys.argv[3])

    if sys.argv[1] in ["G", "Game", "g", "game"]:
        from Game.game import Game

        version_path = "Game/Version%d" % version
        generation_path = "Generation%d" % generation

        try:
            if not os.path.exists(version_path):
                os.makedirs(version_path)
            os.chdir(version_path)

            if not os.path.exists(generation_path):
                os.makedirs(generation_path)
            os.chdir(generation_path)

        except OSError:
            print("Failed to create directory")
            exit(-1)

        game = Game(False, version, generation)
        if len(sys.argv) == 5:
            num_iter = int(sys.argv[4])
        else:
            num_iter = 1000
        game.run_with_encode(num_iter)




if __name__ =="__main__":
    main()