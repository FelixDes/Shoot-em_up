import csv

import pygame

from Scripts.play_mode import Play_mode
from Scripts.settings_class import Settings


def fill_str(name):
    str_dict = {}
    with open(name, encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            str_dict[row[0]] = row[1]
        return str_dict


str_dict = fill_str('Res/CSV/const.csv')
settings_dict = dict()


def update_settings():
    global settings_dict
    settings_dict = fill_str('Res/CSV/settings.csv')


update_settings()
sounds = {}

FIRST_SCREEN = "Res/Audio/first_screen_music.mp3"
BACKGROUND = pygame.image.load("Res/Assets/space.png")
SETTINGS_BUTTON = pygame.transform.scale(pygame.image.load("Res/Assets/settings_button.png"),
                                         (int(str_dict.get('button_x')), int(str_dict.get('button_y'))))
PLAY_BUTTON = pygame.transform.scale(pygame.image.load("Res/Assets/Play.png"),
                                     (int(str_dict.get('Play_button_x')), int(str_dict.get('Play_button_y'))))
BASIC_FONT = pygame.font.SysFont("comicsans", 20)
version_txt = BASIC_FONT.render(str_dict.get('Version'), 1, (255, 255, 255))


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
                pygame.mixer.Channel(i).set_volume(
                    float(settings_dict.get('music_volume') if 'music' in file else settings_dict.get('sound_volume')))
                break
        return
    for i in sounds[file]:
        pygame.mixer.Channel(i).stop()


# Остановка всех звуков
def stop_all_sound():
    for i in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(i).stop()


def main_window():
    global event, settings_dict
    update_settings()
    play_sound(FIRST_SCREEN, -1, True)
    while True:
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Кнопка настроек
                rect_1 = pygame.Rect(0, sc.get_height() - int(str_dict.get('button_y')), int(str_dict.get('button_x')),
                                     int(str_dict.get('button_y')))
                # Кнопка начала
                rect_2 = pygame.Rect(sc.get_width() // 2 - int(str_dict.get('Play_button_x')) // 2,
                                     sc.get_height() // 2 - int(str_dict.get('Play_button_y')) // 2 - 50,
                                     int(str_dict.get('Play_button_x')), int(str_dict.get('Play_button_y')))
                if rect_1.collidepoint(pos):
                    run_settings()
                    settings_dict = fill_str('Res/CSV/settings.csv')
                elif rect_2.collidepoint(pos):
                    stop_all_sound()
                    run_play_mode()
                    update_settings()
                    play_sound(FIRST_SCREEN, -1, True)


def redraw_window():
    pygame.display.update()
    sc.blit(BACKGROUND, (0, 0))
    sc.blit(SETTINGS_BUTTON, (0, sc.get_height() - int(str_dict.get('button_y'))))
    sc.blit(PLAY_BUTTON, (sc.get_width() // 2 - int(str_dict.get('Play_button_x')) // 2,
                          sc.get_height() // 2 - int(str_dict.get('Play_button_y')) // 2 - 50))
    sc.blit(version_txt,
            (((sc.get_width() - version_txt.get_width()) // 2, (sc.get_height() - version_txt.get_height()))))
    # вывод текстовой информации
    # lvl_lable = BASIC_FONT.render(f"Уровень: {self.lvl}", 1, (255, 255, 255))
    # lives_lable = BASIC_FONT.render(f"Жизни: {self.lives}", 1, (255, 255, 255))
    # self.sc.blit(lvl_lable, (self.frame_w - lvl_lable.get_width() - 10, 5))
    # self.sc.blit(lives_lable, (self.frame_w - lives_lable.get_width() - 10, 10 + lvl_lable.get_height()))
    # self.player.draw(self.sc)


# Fixed_all_speeds_and_spawn_chances
# Stable_beta


# Вызов настроек
def run_settings():
    s = Settings(sounds)
    s.run()
    stop_all_sound()
    main_window()


def run_play_mode():
    m = Play_mode()
    m.run()


if __name__ == "__main__":
    pygame.init()
    sc = pygame.display.set_mode((int(str_dict.get("w")), int(str_dict.get("h"))))
    main_window()
    # run_play_mode()
