import csv

import pygame


class Play_mode():
    def __init__(self):
        self.str_dict = {}
        self.fill_str()

        self.FPS = int(self.str_dict.get("FPS"))

    def fill_str(self):
        self.str_dict = {}
        with open('Res/CSV/const.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for index, row in enumerate(reader):
                self.str_dict[row[0]] = row[1]

    def run(self):
        while True:  # обработка нажатий и инициализация игрового поля, спрайтов
            clock = pygame.time.Clock()
            clock.tick(self.FPS)

            # цикл обработки событий
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                elif i.type == pygame.KEYDOWN and i.key == pygame.K_RIGHT:
                    pass
                elif i.type == pygame.KEYDOWN and i.key == pygame.K_LEFT:
                    pass
                elif i.type == pygame.KEYDOWN and (i.key == pygame.K_SPACE or i.key == pygame.K_UP):  # стрельба
                    pass
            pygame.display.update()
