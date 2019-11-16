import os
import sys

sys.path.insert(0, '/content/gdrive/My Drive/Colab Notebooks/')

import Model.run


def main():
    argc = len(sys.argv)
    if argc == 1:
        print("Usage")
        print("[G|Game|g|game version generation num_iter")
        print("[M||m|model]|Model] version generation epoch=1000")


if __name__ =="__main__":
    main()
        