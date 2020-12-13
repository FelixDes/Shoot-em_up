import csv
import random
from math import sqrt

import pygame

pygame.font.init()

str_dict = {}


def fill_str():
    with open('Res/CSV/const.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            str_dict[row[0]] = row[1]


fill_str()

BACKGROUND = pygame.image.load("Res/Assets/space.png")
PLAYER_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/p_ship.png"),
                                         (int(str_dict.get('ship_y')), int(str_dict.get('ship_y'))))
ENEMY_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/enemy.png"),
                                        (int(str_dict.get('ship_x')), int(str_dict.get('ship_y'))))
# BOSS_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/boss_ship.png"), (int(str_dict.get('ship_y')), int(str_dict.get('ship_y'))))
BULLET_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/bul.png"),
                                    (int(str_dict.get('bullet_x')), int(str_dict.get('bullet_y'))))
BASIC_FONT = pygame.font.SysFont("comicsans", 20)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 60)


class Play_mode():
    def __init__(self):
        self.frame_h = int(str_dict.get("h"))
        self.frame_w = int(str_dict.get("w"))
        self.FPS = int(str_dict.get("FPS"))
        self.sc = pygame.display.set_mode((self.frame_w, self.frame_h), pygame.RESIZABLE)
        self.lvl = 0
        self.hp = 4
        self.player_shift = 5
        self.player = Player_Ship(self.frame_w // 2, self.frame_h - int(str_dict.get('ship_y')))
        self.enemies = []
        self.wave_len = 3
        self.enemy_shift = 5
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

    def end_game(self):
        while True:
            self.sc.fill((0, 0, 0))
            game_over_txt = GAME_OVER_FONT.render(f"GAME OVER", 1, (255, 255, 255))
            self.sc.blit(game_over_txt, ((self.frame_w - game_over_txt.get_width()) // 2,
                                         (self.frame_h - game_over_txt.get_height()) // 2))
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            pygame.display.update()

    def run(self):
        while True:
            self.clock.tick(self.FPS)

            if self.hp <= 0 or self.player.hp <= 0:
                self.end_game()

            if len(self.enemies) == 0:
                self.lvl += 1
                self.wave_len += 4
                self.enemy_shift += 1
                for i in range(self.wave_len):
                    enemy = Enemy_Ship(random.randrange(50, self.frame_w - 150), random.randrange(-1500, -100))
                    self.enemies.append(enemy)
            for enemy in self.enemies:
                enemy.draw(self.sc)
            # цикл обработки событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            coef = 1
            keys = pygame.key.get_pressed()
            if list(keys)[79: 83].count(1) == 2:  # срез включает кнопки стрелок
                coef = sqrt(2) / 2
            if keys[pygame.K_RIGHT] and self.player.x + self.player_shift + int(str_dict.get("ship_x")) < self.frame_w:
                self.player.x += self.player_shift * coef
            if keys[pygame.K_LEFT] and self.player.x - self.player_shift > 0:
                self.player.x -= self.player_shift * coef
            if keys[pygame.K_UP] and self.player.y - self.player_shift > 0:
                self.player.y -= self.player_shift * coef
            if keys[pygame.K_DOWN] and self.player.y + self.player_shift + int(str_dict.get("ship_y")) < self.frame_h:
                self.player.y += self.player_shift * coef
            for enemy in self.enemies[:]:
                enemy.mover(self.enemy_shift)
                if enemy.y + int(str_dict.get("ship_y")) > self.frame_h:
                    self.hp -= 1
                    self.enemies.remove(enemy)
            self.redraw_window()

    def redraw_window(self):
        pygame.display.update()
        self.sc.blit(BACKGROUND, (0, 0))
        # вывод текстовой информации
        lvl_lable = BASIC_FONT.render(f"Уровень: {self.lvl}", 1, (255, 255, 255))
        hp_lable = BASIC_FONT.render(f"Жизни: {self.hp}", 1, (255, 255, 255))
        self.sc.blit(lvl_lable, (self.frame_w - lvl_lable.get_width() - 10, 5))
        self.sc.blit(hp_lable, (self.frame_w - hp_lable.get_width() - 10, 10 + lvl_lable.get_height()))
        self.player.draw(self.sc)

    # Проигрывание звуков/музыки
    def play_sound(file):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()


class Super_Ship:
    def __init__(self, x, y, hp=10):
        self.x = x
        self.y = y
        self.hp = hp
        self.ship_asset = ENEMY_SHIP_PNG
        self.bullet_asset = BULLET_PNG
        self.bullets_cool_down = 0
        self.bullets = []

    def draw(self, sc):
        sc.blit(self.ship_asset, (self.x, self.y))


class Player_Ship(Super_Ship):
    def __init__(self, x, y, hp=10):
        super().__init__(x, y, hp)
        self.ship_asset = PLAYER_SHIP_PNG
        self.bullet_asset = BULLET_PNG
        self.mask = pygame.mask.from_surface(self.ship_asset)
        self.max_hp = hp


class Enemy_Ship(Super_Ship):
    def __init__(self, x, y, hp=10):
        super().__init__(x, y, hp)
        self.ship_asset = ENEMY_SHIP_PNG
        self.bullet_asset = BULLET_PNG
        self.mask = pygame.mask.from_surface(self.ship_asset)

    def mover(self, shift):
        self.y += shift
