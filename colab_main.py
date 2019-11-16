import os
import sys

sys.path.insert(0, '/content/gdrive/My Drive/Colab Notebooks/')


def main():
    argc = len(sys.argv)
    if argc == 1:
        print("Usage")
        print("[G|Game|g|game] version generation num_iter")
        print("[M|Mode|m|mode] version generation epoch=1000")


if __name__ =="__main__":
    main()