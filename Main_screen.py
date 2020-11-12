import csv

import pygame

from Scripts.play_mode import Play_mode

str_dict = {}
with open('Res/CSV/const.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for index, row in enumerate(reader):
        str_dict[row[0]] = row[1]


def run_settings():
    pass


def run_play_mode():
    m = Play_mode()
    m.run()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((int(str_dict.get("w")), int(str_dict.get("h"))), pygame.RESIZABLE)
    run_play_mode()
