import json
import os
import sys

DATA_FOLDER: str = None


def GetDataFolder():
    return DATA_FOLDER


def main():
    global DATA_FOLDER

    # Data folder
    path = "/".join(
        os.path.dirname(os.path.realpath(__file__)).split("\\")[:-2]
    )
    DATA_FOLDER = path + "/data/"


main()
