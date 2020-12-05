import csv

import pygame

pygame.font.init()

str_dict = {}


def fill_str():
    with open('Res/CSV/const.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            str_dict[row[0]] = row[1]


fill_str()

BACKGROUND = pygame.transform.rotate(pygame.image.load("Res/Assets/space.png"), 90)
PLAYER_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/p_ship.png"),
                                         (int(str_dict.get('ship_y')), int(str_dict.get('ship_y'))))
ENEMY_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/enemy.png"),
                                        (int(str_dict.get('ship_x')), int(str_dict.get('ship_y'))))
# BOSS_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/boss_ship.png"), (int(str_dict.get('ship_y')), int(str_dict.get('ship_y'))))
BULLET_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/bul.png"),
                                    (int(str_dict.get('bullet_x')), int(str_dict.get('bullet_y'))))
BASIC_FONT = pygame.font.SysFont("comicsans", 20)


class Play_mode():
    def __init__(self):
        self.frame_h = int(str_dict.get("h"))
        self.frame_w = int(str_dict.get("w"))
        self.FPS = int(str_dict.get("FPS"))
        self.sc = pygame.display.set_mode((self.frame_w, self.frame_h), pygame.RESIZABLE)
        self.lvl = 1
        self.hp = 4
        self.player_shift = 5
        self.player = Player_Ship(self.frame_w//2, self.frame_h-int(str_dict.get('ship_y')))

    def run(self):
        while True:
            clock = pygame.time.Clock()
            clock.tick(self.FPS)
            self.redraw_window()
            # цикл обработки событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.player.x + self.player_shift + int(str_dict.get("ship_x")) < self.frame_w:
                self.player.x += self.player_shift
            elif keys[pygame.K_LEFT] and self.player.x - self.player_shift > 0:
                self.player.x -= self.player_shift
            elif keys[pygame.K_UP] and self.player.y - self.player_shift > 0:
                self.player.y -= self.player_shift
            elif keys[pygame.K_DOWN] and self.player.y + self.player_shift + int(str_dict.get("ship_y")) < self.frame_h:
                self.player.y += self.player_shift

    def redraw_window(self):
        pygame.display.update()
        self.sc.blit(BACKGROUND, (0, 0))
        # вывод текстовой информации
        lvl_lable = BASIC_FONT.render(f"Уровень: {self.lvl}", 1, (255, 255, 255))
        hp_lable = BASIC_FONT.render(f"Жизни: {self.hp}", 1, (255, 255, 255))
        self.sc.blit(lvl_lable, (self.frame_w - lvl_lable.get_width() - 10, 5))
        self.sc.blit(hp_lable, (self.frame_w - hp_lable.get_width() - 10, 10 + lvl_lable.get_height()))
        self.player.draw(self.sc)


class Super_Ship:
    def __init__(self, x, y, hp=100):
        self.x = x
        self.y = y
        self.hp = hp
        self.ship_asset = ENEMY_SHIP_PNG
        self.bullets_cool_down = 0
        self.bullets = []

    def draw(self, sc):
        sc.blit(self.ship_asset, (self.x, self.y))


class Player_Ship(Super_Ship):
    def __init__(self, x, y, hp=1):
        super().__init__(x, y, hp)
        self.ship_asset = PLAYER_SHIP_PNG
        self.bullet_asset = BULLET_PNG