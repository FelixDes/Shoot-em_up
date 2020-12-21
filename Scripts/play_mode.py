import csv
import random
import sys
import threading
import time
from math import sqrt

import pygame

pygame.font.init()


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
# Словарь со звуками
sounds = dict()
BACKGROUND = pygame.image.load("Res/Assets/space.png")
PLAYER_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/player.png"),
                                         (int(str_dict.get('ship_y')), int(str_dict.get('ship_y'))))
ENEMY_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/enemy.png"),
                                        (int(str_dict.get('ship_x')), int(str_dict.get('ship_y'))))
BOSS_SHIP_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/boss.png"),
                                       (int(str_dict.get('ship_y')), int(str_dict.get('ship_y'))))
BULLET_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/bullet.png"),
                                    (int(str_dict.get('bullet_x')), int(str_dict.get('bullet_y'))))
BATTLE_MUSIC = "Res/Audio/battle_music.mp3"
DAMAGE_SOUND = "Res/Audio/damage.mp3"
DEATH_SOUND = "Res/Audio/death_sound.mp3"
SHOOT_SOUND = "Res/Audio/shoot.mp3"
BASIC_FONT = pygame.font.SysFont("comicsans", 20)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 60)

exit_flag = False


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


def exit_for_time(t):
    global exit_flag
    time.sleep(t)
    exit_flag = True
    sys.exit()


class Play_mode():
    def __init__(self):
        self.frame_h = int(str_dict.get("h"))
        self.frame_w = int(str_dict.get("w"))
        self.FPS = int(str_dict.get("FPS"))
        self.sc = pygame.display.set_mode((self.frame_w, self.frame_h), pygame.RESIZABLE)
        self.lvl = 0
        self.lives = 4
        self.player_shift = 7
        self.player = Player_Ship(self.frame_w // 2, self.frame_h - int(str_dict.get('ship_y')))
        self.enemies = []
        self.wave_len = 0
        self.enemy_shift = 5
        self.bull_shift = 7
        self.clock = pygame.time.Clock()
        update_settings()
        # Инициализация миксера с 50 каналами для звуков
        pygame.mixer.init()
        pygame.mixer.set_num_channels(50)

    def end_game(self):
        global exit_flag
        time = 4

        # _thread.start_new_thread(exit_for_time, (time,))
        exit_tread = threading.Thread(target=exit_for_time, args=(time,))
        exit_tread.start()
        stop_all_sound()
        play_sound(DEATH_SOUND, 0, True)
        # exit_tread.join()
        while True:

            self.sc.fill((0, 0, 0))
            game_over_txt = GAME_OVER_FONT.render(f"GAME OVER", 1, (255, 255, 255))
            self.sc.blit(game_over_txt, ((self.frame_w - game_over_txt.get_width()) // 2,
                                         (self.frame_h - game_over_txt.get_height()) // 2))
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or exit_flag:
                    exit_flag = False
                    exit(0)

            pygame.display.update()

    def run(self):
        play_sound(BATTLE_MUSIC, -1, True)
        while True:
            self.clock.tick(self.FPS)

            if self.lives <= 0 or self.player.hp <= 0:
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
                # pass
            # Выход
            if keys[pygame.K_ESCAPE]:
                stop_all_sound()
                break

            if keys[pygame.K_RIGHT] and self.player.x + self.player_shift + int(str_dict.get("ship_x")) < self.frame_w:
                self.player.x += self.player_shift * coef
            if keys[pygame.K_LEFT] and self.player.x - self.player_shift > 0:
                self.player.x -= self.player_shift * coef
            if keys[pygame.K_UP] and self.player.y - self.player_shift > 0:
                self.player.y -= self.player_shift * coef
            if keys[pygame.K_DOWN] and self.player.y + self.player_shift + int(str_dict.get("ship_y")) < self.frame_h:
                self.player.y += self.player_shift * coef
            if keys[pygame.K_SPACE]:
                self.player.shoot()
            for enemy in self.enemies[:]:
                enemy.mover(self.enemy_shift)
                enemy.move_bullets(self.bull_shift, self.player)

                if random.randrange(0, 120) == 1 and enemy.y > 0:
                    enemy.shoot()

                if collide(enemy, self.player):
                    self.player.hp -= 10
                    play_sound(DAMAGE_SOUND, 0, True)
                    self.enemies.remove(enemy)

                if enemy.y + int(str_dict.get("ship_y")) > self.frame_h:
                    self.lives -= 1
                    self.enemies.remove(enemy)

            self.player.move_bullets(-self.bull_shift, self.enemies)
            self.redraw_window()

    def redraw_window(self):
        pygame.display.update()
        self.sc.blit(BACKGROUND, (0, 0))
        # вывод текстовой информации
        lvl_lable = BASIC_FONT.render(f"Уровень: {self.lvl}", 1, (255, 255, 255))
        lives_lable = BASIC_FONT.render(f"Жизни: {self.lives}", 1, (255, 255, 255))
        self.sc.blit(lvl_lable, (self.frame_w - lvl_lable.get_width() - 10, 5))
        self.sc.blit(lives_lable, (self.frame_w - lives_lable.get_width() - 10, 10 + lvl_lable.get_height()))
        self.player.draw(self.sc)


class Super_Bullet:
    def __init__(self, x, y):
        self.x = x + 17
        self.y = y
        self.img = BULLET_PNG
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, sc):
        sc.blit(self.img, (self.x, self.y))

    def mover(self, shift):
        self.y += shift

    def off_screen(self, h):
        return not (h > self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None


class Super_Ship:
    COOLDOWN = 15

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
        for bullet in self.bullets:
            bullet.draw(sc)

    def move_bullets(self, shift, obj):
        self.cool_down()
        for bullet in self.bullets:
            bullet.mover(shift)
            if bullet.off_screen(int(str_dict.get('h'))):
                self.bullets.remove(bullet)
                play_sound(DAMAGE_SOUND, 0, True)
            elif bullet.collision(obj):
                play_sound(DAMAGE_SOUND, 0, True)
                obj.hp -= 10
                self.bullets.remove(bullet)

    def cool_down(self):
        if self.bullets_cool_down >= self.COOLDOWN:
            self.bullets_cool_down = 0
        elif self.bullets_cool_down > 0:
            self.bullets_cool_down += 1

    def shoot(self):
        if self.bullets_cool_down == 0:
            play_sound(SHOOT_SOUND, 0, True)
            bullet = Super_Bullet(self.x, self.y)
            self.bullets.append(bullet)
            self.bullets_cool_down = 1


class Player_Ship(Super_Ship):
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.ship_asset = PLAYER_SHIP_PNG
        self.bullet_asset = BULLET_PNG
        self.mask = pygame.mask.from_surface(self.ship_asset)
        self.max_hp = hp

    def move_bullets(self, shift, objs):
        self.cool_down()
        for bullet in self.bullets:
            bullet.mover(shift)
            if bullet.off_screen(int(str_dict.get('h'))):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_asset.get_height() + 10, self.ship_asset.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_asset.get_height() + 10,
                                               self.ship_asset.get_width() * (self.hp / self.max_hp), 10))

    def draw(self, sc):
        super().draw(sc)
        self.healthbar(sc)


class Enemy_Ship(Super_Ship):
    def __init__(self, x, y, hp=99999999999):
        super().__init__(x, y, hp)
        self.ship_asset = ENEMY_SHIP_PNG
        self.bullet_asset = BULLET_PNG
        self.mask = pygame.mask.from_surface(self.ship_asset)

    def mover(self, shift):
        self.y += shift
