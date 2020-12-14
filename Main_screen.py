import csv

import pygame

from Scripts.play_mode import Play_mode

# Инициализация миксера с 50 каналами для звуков
pygame.mixer.init()
pygame.mixer.set_num_channels(50)

# Словарь со звуками
sounds = dict()
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


# Проигрывание звуков/музыки, чтобы музыка повторялась в loops надо передать -1,
# start_sound - флаг, отвечающий за действие метода (False - выключение звуков, True - включение)
def play_sound(file, loops=0, start_sound=False):
    if start_sound:
        for i in range(pygame.mixer.get_num_channels()):
            if not pygame.mixer.Channel(i).get_busy():
                if file not in sounds.keys():
                    sounds[file] = [i]
                else:
                    sounds[file].append(i)
                pygame.mixer.Channel(i).play(pygame.mixer.Sound(file), loops=loops)
            break
        return
    for i in sounds[file]:
        pygame.mixer.Channel(i).stop()


# Остановка всех звуков
def stop_all_sound():
    for i in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(i).stop()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((int(str_dict.get("w")), int(str_dict.get("h"))), pygame.RESIZABLE)
    run_play_mode()
