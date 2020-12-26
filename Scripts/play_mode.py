import csv
import random
import threading
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
ENEMY_BULLET_PNG = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("Res/Assets/bullet.png"),
                                                                  (int(str_dict.get('bullet_x')),
                                                                   int(str_dict.get('bullet_y')))), 180)
BOOSTER_PNG = pygame.transform.scale(pygame.image.load("Res/Assets/power_up.png"),
                                     (int(str_dict.get('booster_x')), int(str_dict.get('booster_y'))))
ICON = ENEMY_SHIP_PNG
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


class Play_mode():
    def __init__(self):
        self.frame_h = int(str_dict.get("h"))
        self.frame_w = int(str_dict.get("w"))
        self.FPS = int(str_dict.get("FPS"))
        self.sc = pygame.display.set_mode((self.frame_w, self.frame_h))
        pygame.display.set_caption(str_dict.get("Name"))
        pygame.display.set_icon(ICON)
        self.lvl = 0
        self.player = Player_Ship(self.frame_w // 2 - int(str_dict.get('ship_x')) // 2,
                                  self.frame_h - int(str_dict.get('ship_y')) - 30)
        self.enemies = pygame.sprite.Group()
        self.boosters = pygame.sprite.Group()
        self.wave_len = 0
        self.enemy_shift = 2
        self.bull_shift = 7
        self.clock = pygame.time.Clock()
        update_settings()
        # Инициализация миксера с 50 каналами для звуков
        pygame.mixer.init()
        pygame.mixer.set_num_channels(50)

    def end_game(self):
        global exit_flag
        time = 4
        stop_all_sound()
        play_sound(DEATH_SOUND, 0, True)
        lost_count = 0
        # exit_tread.join()
        while True:
            lost_count += 1
            if lost_count > int(str_dict.get("FPS")) * 3:
                with open('Main_screen.py', "r") as file:
                    exec(file.read())
                    exit()

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
            self.player.shoot()
            self.clock.tick(self.FPS)

            if self.player.lives <= 0 or self.player.hp <= 0:
                self.end_game()

            if len(self.enemies) == 0:
                self.lvl += 1
                self.wave_len += 1
                self.bull_shift += 1
                if self.wave_len == 6:
                    self.player.lives += 1
                if self.wave_len > 5 and self.wave_len % 2 != 0:
                    self.player.speed += 1
                if self.enemy_shift != 7:
                    self.enemy_shift += 1
                for i in range(self.wave_len):
                    enemy = Enemy_Ship(random.randrange(50, self.frame_w - 50), random.randrange(-1500, -100))
                    self.enemies.add(enemy)
            # Создвние бустеров
            rand = random.randint(0, 2500)
            if rand == 1:
                self.boosters.add(Live_Booster(random.randint(50, self.frame_w - 50), self.enemy_shift))
            elif rand == 2:
                self.boosters.add(Health_Booster(random.randint(50, self.frame_w - 50), self.enemy_shift))
            elif rand == 3:
                self.boosters.add(Speed_Booster(random.randint(50, self.frame_w - 50), self.enemy_shift))
            elif rand == 4 and self.player.COOLDOWN > 7:
                self.boosters.add(Damage_Booster(random.randint(50, self.frame_w - 50), self.enemy_shift))
            elif rand == 5 and self.player.bullet_amount < 5:
                self.boosters.add(Gun_Booster(random.randint(50, self.frame_w - 50), self.enemy_shift))
            self.enemies.draw(self.sc)
            self.boosters.draw(self.sc)
            for booster in self.boosters:
                booster.move()
                if collide(booster, self.player):
                    booster.player_collision(self.player)
                    self.boosters.remove(booster)
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

            if keys[pygame.K_RIGHT] and self.player.rect.x + self.player.speed + int(
                    str_dict.get("ship_x")) < self.frame_w:
                self.player.rect.x += self.player.speed * coef
            if keys[pygame.K_LEFT] and self.player.rect.x - self.player.speed > 0:
                self.player.rect.x -= self.player.speed * coef
            if keys[pygame.K_UP] and self.player.rect.y - self.player.speed > 0:
                self.player.rect.y -= self.player.speed * coef
            if keys[pygame.K_DOWN] and self.player.rect.y + self.player.speed + int(
                    str_dict.get("ship_y")) < self.frame_h:
                self.player.rect.y += self.player.speed * coef
            # if keys[pygame.K_SPACE]:
            #     self.player.shoot()
            for enemy in self.enemies:
                enemy.mover(self.enemy_shift)
                enemy.move_bullets(self.bull_shift, self.player)

                if random.randrange(0, 120) == 1 and enemy.rect.y > 0:
                    enemy.shoot()

                if collide(enemy, self.player):
                    self.player.hp -= 10
                    play_sound(DAMAGE_SOUND, 0, True)
                    self.enemies.remove(enemy)

                if enemy.rect.y + int(str_dict.get("ship_y")) > self.frame_h:
                    self.player.lives -= 1
                    self.enemies.remove(enemy)

            self.player.move_bullets(-self.bull_shift, self.enemies)
            self.redraw_window()

    def redraw_window(self):
        pygame.display.update()
        self.sc.blit(BACKGROUND, (0, 0))
        # вывод текстовой информации
        lvl_lable = BASIC_FONT.render(f"Уровень: {self.lvl}", 1, (255, 255, 255))
        lives_lable = BASIC_FONT.render(f"Жизни: {self.player.lives}", 1, (255, 255, 255))
        self.sc.blit(self.player.image, self.player.rect)
        self.player.healthbar(self.sc)
        self.player.bullets.draw(self.sc)
        self.enemies.draw(self.sc)
        for enemy in self.enemies:
            enemy.bullets.draw(self.sc)
        self.sc.blit(lvl_lable, (self.frame_w - lvl_lable.get_width() - 10, 5))
        self.sc.blit(lives_lable, (self.frame_w - lives_lable.get_width() - 10, 10 + lvl_lable.get_height()))


class Super_Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def mover(self, shift):
        self.y += shift
        self.rect.y += shift

    def off_screen(self, h):
        return not (h > self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None


class Super_Ship(pygame.sprite.Sprite):


    def __init__(self, x, y, hp=10):
        super().__init__()
        self.hp = hp
        self.COOLDOWN = 13
        self.damage = 10
        self.image = ENEMY_SHIP_PNG
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.bullet_asset = BULLET_PNG
        self.bullets_cool_down = 0
        self.bullets = pygame.sprite.Group()
        self.bullet_amount = 1

    def move_bullets(self, shift, obj):
        self.cool_down()
        for bullet in self.bullets:
            bullet.mover(shift)
            if bullet.off_screen(int(str_dict.get('h'))):
                self.bullets.remove(bullet)
                play_sound(DAMAGE_SOUND, 0, True)
            elif bullet.collision(obj):
                play_sound(DAMAGE_SOUND, 0, True)
                obj.hp -= self.damage
                self.bullets.remove(bullet)

    def cool_down(self):
        if self.bullets_cool_down >= self.COOLDOWN:
            self.bullets_cool_down = 0
        elif self.bullets_cool_down > 0:
            self.bullets_cool_down += 1

    def shoot(self):
        if self.bullets_cool_down == 0:
            play_sound(SHOOT_SOUND, 0, True)
            if self.bullet_amount != 1:
                for i in range(1, self.bullet_amount):
                    if i % 2 != 0:
                        bullet = Super_Bullet(self.rect.x + 25 + i * 10, self.rect.y + 20, self.bullet_image)
                        self.bullets.add(bullet)
                for i in range(1, self.bullet_amount):
                    if i % 2 != 0:
                        bullet = Super_Bullet(self.rect.x + 25 - i * 10, self.rect.y + 20, self.bullet_image)
                        self.bullets.add(bullet)
            bullet = Super_Bullet(self.rect.x + 25, self.rect.y + 20, self.bullet_image)
            self.bullets.add(bullet)
            self.bullets_cool_down = 1


class Super_Booster(pygame.sprite.Sprite):
    def __init__(self, image, x, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.x, self.y = x, self.rect.y
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.y += self.speed
        self.y = self.rect.y


class Health_Booster(Super_Booster):
    def __init__(self, x, speed):
        super().__init__(BOOSTER_PNG, x, speed)

    def player_collision(self, player):
        if player.hp < player.max_hp:
            player.hp += random.randint(20, 50)
        if player.hp > player.max_hp:
            player.hp = player.max_hp


class Live_Booster(Super_Booster):
    def __init__(self, x, speed):
        super().__init__(BOOSTER_PNG, x, speed)

    def player_collision(self, player):
        player.lives += 1


class Gun_Booster(Super_Booster):
    def __init__(self, x, speed):
        super().__init__(BOOSTER_PNG, x, speed)

    def player_collision(self, player):
        if player.bullet_amount <= 5:
            player.bullet_amount += 2


class Speed_Booster(Super_Booster):
    def __init__(self, x, speed):
        super().__init__(BOOSTER_PNG, x, speed)

    def player_collision(self, player):
        player.speed = 12
        t = threading.Timer(5.0, self.normalize, args=(player,))
        t.start()

    def normalize(self, player):
        player.speed = 7


class Damage_Booster(Super_Booster):
    def __init__(self, x, speed):
        super().__init__(BOOSTER_PNG, x, speed)

    def player_collision(self, player):
        if player.COOLDOWN >= 7:
            player.COOLDOWN -= 1
    #     player.damage = 20
    #     t = threading.Timer(5.0, self.normalize, args=(player,))
    #     t.start()
    #
    # def normalize(self, player):
    #     player.damage = 10


class Player_Ship(Super_Ship):
    def __init__(self, x, y, hp=100):
        super().__init__(x, y, hp)
        self.image = PLAYER_SHIP_PNG
        self.bullet_image = BULLET_PNG
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.max_hp = hp
        self.lives = 1
        self.speed = 7
        self.bullet_amount = 1

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
                         (self.rect.x, self.rect.y + self.image.get_height() + 10, self.image.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.rect.x, self.rect.y + self.image.get_height() + 10,
                                               self.image.get_width() * (self.hp / self.max_hp), 10))


class Enemy_Ship(Super_Ship):
    def __init__(self, x, y, hp=15):
        super().__init__(x, y, hp)
        self.image = ENEMY_SHIP_PNG
        self.bullet_image = ENEMY_BULLET_PNG
        self.mask = pygame.mask.from_surface(self.image)

    def mover(self, shift):
        self.rect.y += shift
