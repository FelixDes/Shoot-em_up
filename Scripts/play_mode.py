import csv

import pygame


class Play_mode():
    def __init__(self):
        self.str_dict = {}
        self.fill_str()
        self.field = []

        self.player_x_from_list = 0
        self.field_h = int(self.str_dict.get("field_h"))
        self.field_w = int(self.str_dict.get("field_w"))
        self.frame_h = int(self.str_dict.get("h"))
        self.frame_w = int(self.str_dict.get("w"))

        self.FPS = int(self.str_dict.get("FPS"))

        self.BACK = "Res/Assets/space.png"

        self.fill_field()

    def fill_field(self):
        self.field = [[0 for j in range(self.field_w)]
                      for i in range(self.field_h)]
        self.field[-1][len(self.field[-1]) // 2] = "p"

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
                    self.p_do(1)
                elif i.type == pygame.KEYDOWN and i.key == pygame.K_LEFT:
                    self.p_do(-1)
                elif i.type == pygame.KEYDOWN and (i.key == pygame.K_SPACE or i.key == pygame.K_UP):  # стрельба
                    self.p_do(0)
            self.draw_all()
            pygame.display.update()

    def draw_all(self):
        background_surf = pygame.image.load(self.BACK)
        screen = pygame.display.set_mode((self.frame_w, self.frame_h), pygame.RESIZABLE)
        screen.blit(background_surf, (0, 0))


    def p_do(self, dir):
        index_p = self.field[-1].index("p")
        if dir == 1 and 0 <= self.field[-1].index("p") <= int(self.str_dict.get('field_w')) - 2:
            self.field[-1][index_p], self.field[-1][index_p + 1] = self.field[-1][index_p + 1], self.field[-1][
                index_p]
            print(self.field)
            self.player_x_from_list += 1 / self.field_w * self.frame_w
        elif dir == -1 and 1 <= self.field[-1].index("p") <= int(self.str_dict.get('field_w')) - 1:
            self.field[-1][index_p], self.field[-1][index_p - 1] = self.field[-1][index_p - 1], self.field[-1][
                index_p]
            print(self.field)
            self.player_x_from_list -= 1 / self.field_w * self.frame_w
