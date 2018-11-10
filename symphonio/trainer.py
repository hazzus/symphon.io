"""
File for basic machine training
Photos in directory basic_train_data are splitted by composer id
Here is the list of corresponding:
0. Tchaikovsky
1. Rakhmaninov
2. Bach
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "symphonio.settings")
django.setup()

from compface.models import Composer, add_composer_encoding

import PIL.Image

path = "basic_train_data"


def train_for_dir(dirpath, dir):
    print(dir)
    for file in os.listdir(dirpath + os.sep + dir):
        print(file)
        add_composer_encoding(dir, PIL.Image.open(open(dirpath + os.sep + dir + os.sep + file, "rb")))


def basic_train():
    for (dirpath, dirnames, filenames) in os.walk(path):
        for dir in dirnames:
            train_for_dir(dirpath, dir)


if __name__ == '__main__':
    basic_train()
