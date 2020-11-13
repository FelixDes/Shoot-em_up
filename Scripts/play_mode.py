import csv

import pygame


class Play_mode():
    def __init__(self):
        self.str_dict = {}
        self.fill_str()
        self.field = []

        self.FPS = int(self.str_dict.get("FPS"))

    def fill_field(self):
        self.field = [0] * int(self.str_dict.get("field_h"))
        for i in range(int(self.str_dict.get("field_h"))):
            self.field[i] = [0] * int(self.str_dict.get("field_w"))
        self.field[-1][self.field[-1] // 2] = "p"

    def fill_str(self):
        self.str_dict = {}
        with open('Res/CSV/const.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
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
