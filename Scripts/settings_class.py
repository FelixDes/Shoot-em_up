import csv

import pygame
# Класс для слайдера. В будущем возможно прийдётся самим сделать.
from pygame_widgets import Slider


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
BACKGROUND = pygame.image.load("Res/Assets/space.png")
SETTINGS_BUTTON = pygame.transform.scale(pygame.image.load("Res/Assets/settings_button.png"),
                                         (int(str_dict.get('button_x')), int(str_dict.get('button_y'))))


class Settings():
    def __init__(self, sounds):
        self.frame_h = int(str_dict.get("h"))
        self.frame_w = int(str_dict.get("w"))
        self.sc = pygame.display.set_mode((self.frame_w, self.frame_h), pygame.RESIZABLE)

        self.mus_curr_vol = 0
        self.snd_curr_vol = 0
        self.sounds = sounds
        # Инициализация слайдеров, координаты наверное можно лучше сделать
        self.sound_vol_slider = Slider(self.sc, self.frame_w * 2 // 5, self.frame_h * 1 // 10, 100, 20,
                                       colour=(100, 100, 100), handleColour=(40, 40, 40))
        self.music_vol_slider = Slider(self.sc, self.frame_w * 2 // 5, self.frame_h * 2 // 10, 100, 20,
                                       colour=(100, 100, 100), handleColour=(40, 40, 40))
        update_settings()
        print(settings_dict)
        print(int(float(settings_dict.get('music_volume')) * 100), int(float(settings_dict.get('sound_volume')) * 100))
        self.sound_vol_slider.setValue(int(float(settings_dict.get('sound_volume')) * 100))
        self.music_vol_slider.setValue(int(float(settings_dict.get('music_volume')) * 100))

    def run(self):
        global event
        while True:
            events = pygame.event.get()
            self.music_vol_slider.listen(events)
            self.sound_vol_slider.listen(events)

            self.redraw_window()
            for event in events:
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    rect = pygame.Rect(0, self.sc.get_height() - int(str_dict.get('button_y')),
                                       int(str_dict.get('button_x')),
                                       int(str_dict.get('button_y')))
                    # Выход из настроек. Сохранение настроек.
                    if rect.collidepoint(pos):
                        with open('Res/CSV/settings.csv', encoding="utf8") as csvfile:
                            change, write = dict(), list()
                            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                            for row in reader:
                                change[row[0]] = row[1]
                            # В change записываются изменённые настройки
                            change['music_volume'] = self.music_vol_slider.getValue() / 100
                            change['sound_volume'] = self.sound_vol_slider.getValue() / 100
                            write = list(map(lambda x: [x, change[x]], change.keys()))
                            writer = csv.writer(open('Res/CSV/settings.csv', 'w', encoding="utf8", newline=''),
                                                delimiter=',', quoting=csv.QUOTE_ALL)
                            writer.writerows(write)
                        return

    def redraw_window(self):
        # Текст около слайдеров
        font = pygame.font.Font(None, 50)
        sound_text = font.render("Sound:", True, (170, 170, 170))
        music_text = font.render("Music:", True, (170, 170, 170))

        self.sc.blit(BACKGROUND, (0, 0))
        self.sc.blit(SETTINGS_BUTTON, (0, self.sc.get_height() - int(str_dict.get('button_y'))))
        # Текст около слайдеров
        self.sc.blit(sound_text, (self.frame_w * 1 // 10 - 10, self.frame_h * 1 // 10 - 10))
        self.sc.blit(music_text, (self.frame_w * 1 // 10 - 1, self.frame_h * 2 // 10 - 10))

        self.music_vol_slider.draw()
        self.sound_vol_slider.draw()
        # Изменение громкости если значение было изменено
        if self.mus_curr_vol != self.music_vol_slider.getValue():
            self.change_volume(music=True, volume=self.music_vol_slider.getValue())
            self.mus_curr_vol = self.music_vol_slider.getValue()
        if self.snd_curr_vol != self.sound_vol_slider.getValue():
            self.change_volume(music=False, volume=self.sound_vol_slider.getValue())
            self.snd_curr_vol = self.sound_vol_slider.getValue()
        pygame.display.update()

    # Изменение громкости, music - отвечает за тип звуков (True - изменение громкости музыки, False - остальных звуков)
    def change_volume(self, music=False, volume=99):
        volume /= 100
        for i in self.sounds.keys():
            if not (music ^ ('music' in i)):
                for j in self.sounds[i]:
                    pygame.mixer.Channel(j).set_volume(volume)
