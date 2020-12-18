import csv

import pygame

from Scripts.play_mode import Play_mode

str_dict = {}
sounds = {}
with open('Res/CSV/const.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        str_dict[row[0]] = row[1]

FIRST_SCREEN = "Res/Audio/first_screen.mp3"
BACKGROUND = pygame.image.load("Res/Assets/space.png")
MAIN_BUTTON = pygame.transform.scale(pygame.image.load("Res/Assets/main_button.png"),
                                     (int(str_dict.get('button_x')), int(str_dict.get('button_y'))))
PLAY_BUTTON = pygame.transform.scale(pygame.image.load("Res/Assets/Play.png"),
                                     (int(str_dict.get('Play_button_x')), int(str_dict.get('Play_button_y'))))


def run_settings():
    pass


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


def main_window():
    global event
    play_sound(FIRST_SCREEN, -1, True)
    while True:
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # rect = pygame.Rect(0, sc.get_height() - int(str_dict.get('button_y')), int(str_dict.get('button_x')),
            #                    int(str_dict.get('button_y')))
            rect = pygame.Rect(sc.get_width() // 2 - int(str_dict.get('Play_button_x')) // 2,
                               sc.get_height() // 2 - int(str_dict.get('Play_button_y')) // 2 - 50,
                               int(str_dict.get('Play_button_x')), int(str_dict.get('Play_button_y')))
            if rect.collidepoint(pos):
                stop_all_sound()
                run_play_mode()


def redraw_window():
    pygame.display.update()
    sc.blit(BACKGROUND, (0, 0))
    sc.blit(MAIN_BUTTON, (0, sc.get_height() - int(str_dict.get('button_y'))))
    sc.blit(PLAY_BUTTON, (sc.get_width() // 2 - int(str_dict.get('Play_button_x'))//2, sc.get_height() // 2 - int(str_dict.get('Play_button_y'))//2 - 50))
    # вывод текстовой информации
    # lvl_lable = BASIC_FONT.render(f"Уровень: {self.lvl}", 1, (255, 255, 255))
    # lives_lable = BASIC_FONT.render(f"Жизни: {self.lives}", 1, (255, 255, 255))
    # self.sc.blit(lvl_lable, (self.frame_w - lvl_lable.get_width() - 10, 5))
    # self.sc.blit(lives_lable, (self.frame_w - lives_lable.get_width() - 10, 10 + lvl_lable.get_height()))
    # self.player.draw(self.sc)


def stop_all_sound():
    for i in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(i).stop()


def run_play_mode():
    m = Play_mode()
    m.run()


if __name__ == "__main__":
    pygame.init()
    sc = pygame.display.set_mode((int(str_dict.get("w")), int(str_dict.get("h"))), pygame.RESIZABLE)
    main_window()
    # run_play_mode()
