import csv

import pygame

from Scripts.play_mode import Play_mode

# Инициализация миксера с 50 каналами для звуков
pygame.mixer.init()
pygame.mixer.set_num_channels(50)

str_dict = {}
with open('Res/CSV/const.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        str_dict[row[0]] = row[1]


def run_settings():
    pass


def run_play_mode():
    m = Play_mode()
    m.run()


# Проигрывание звуков/музыки, чтобы музыка повторялась в loops надо передать -1
def play_sound(file, loops=0):
    for i in range(pygame.mixer.get_num_channels()):
        if not pygame.mixer.Channel(i).get_busy():
            pygame.mixer.Channel(i).play(pygame.mixer.Sound(file), loops=loops)
            break


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((int(str_dict.get("w")), int(str_dict.get("h"))), pygame.RESIZABLE)
    run_play_mode()
