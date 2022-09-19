from copy import deepcopy
import random
import pygame


W, H = 10, 20
size_tile = 30
game_res = W * size_tile, H * size_tile
size_window = 540, 640
game_fps = 60
side_generation = ['0', '3']
game_end = 0
game_score = 0
plus_score = 10
level_game = 1
scores = 0
speed_game = 5

pygame.init()
sc = pygame.display.set_mode(size_window)
game_sc = pygame.Surface(game_res)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * size_tile, y * size_tile,
                    size_tile, size_tile, outlines="1")
                        for x in range(W) for y in range(H)]

# кординаты машинок и бортов
cordinat_car = [(-1, 0), (-2, 0), (-3, 0), (-2, -1), (-2, 1), (-3, 2), (-1, 2)]
cordinat_borders = [
    (4, 0), (4, -1), (-5, 0), (-5, -1), (4, -3), (4, -4), (-5, -3), (-5, -4),
    (4, -6), (4, -7), (-5, -6), (-5, -7), (4, -9), (4, -10), (-5, -9),
    (-5, -10), (4, -12), (4, -13), (-5, -12), (-5, -13), (4, -15), (4, -16),
    (-5, -15), (-5, -16), (4, -18), (4, -19), (-5, -18), (-5, -19)
]
enemy_car = [pygame.Rect(x + W // 2, y - 5, 1, 1) for x, y in cordinat_car]
enemy_car2 = [pygame.Rect(x + W // 2, y - 15, 1, 1) for x, y in cordinat_car]
enemy_car3 = [pygame.Rect(x + W // 2, y - 24, 1, 1) for x, y in cordinat_car]
figure_car = [pygame.Rect(x + W // 2, y + 17, 1, 1) for x, y in cordinat_car]
figure_borders = [pygame.Rect(x + W // 2, y + 1, 1, 1)
                            for x, y in cordinat_borders]

figure_rect = pygame.Rect(0, 0, size_tile - 2, size_tile - 2)

anim_count, anim_speed, anim_limit = 0, 100, 2000

fon = pygame.image.load('fon.png').convert()
game_fon = pygame.image.load('game_fon.png').convert()

# настройка шрифтов
myfont = pygame.font.SysFont("monospace", 65)
myfont1 = pygame.font.SysFont("monospace", 35)
title_races = myfont.render('Races', True, pygame.Color('white'))
title_score = myfont1.render('score:', True, pygame.Color('red'))
title_level = myfont1.render('level:', True, pygame.Color('green'))
title_speed = myfont1.render('speed:', True, pygame.Color('green'))
title_hi_score = myfont1.render('hi-score:', True, pygame.Color('red'))


# проверка на границы
def check_borders():
    if (figure_car[i].x < 0 or figure_car[i].x > W-1
            or figure_car[i].y < 0 or figure_car[i].y > H-1):
        return False
    return True


# проверка на аварию
def check_enemy_car():
    if (figure_car[i].x == enemy_car[j].x
            and figure_car[i].y == enemy_car[j].y):
        return False
    if (figure_car[i].x == enemy_car2[j].x
            and figure_car[i].y == enemy_car2[j].y):
        return False
    if (figure_car[i].x == enemy_car3[j].x
            and figure_car[i].y == enemy_car3[j].y):
        return False
    return True


# конец игры
def game_over():
    for i in range(28):
        figure_borders[i].y -= 20
    for k in range(7):
        enemy_car[k].y -= 20
    for k in range(7):
        enemy_car2[k].y -= 20
    for k in range(7):
        enemy_car3[k].y -= 20


# сохранение рекорда
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


# проверка текущего рекорда
def set_record(record, game_score):
    rec = max(int(record), game_score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    hi_score = get_record()
    LR = 0
    sc.blit(fon, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_fon, (0, 0))

    # очки,уровни,скорость
    if game_score - scores > 200:
        level_game += 1
        scores = game_score
        if level_game % 5 == 0:
            speed_game += 5
            plus_score += 10
            anim_speed += 20

    # управление клавишами
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                LR = -3
            elif event.key == pygame.K_RIGHT:
                LR = 3

    # управление машинкой, проверка на барьер
    figure_old = deepcopy(figure_car)
    for i in range(7):
        figure_car[i].x += LR
        if not check_borders():
            figure_car = deepcopy(figure_old)
            break

    # проверка на аварию
    for j in range(7):
        for i in range(7):
            if not check_enemy_car():
                [pygame.draw.rect(game_sc, pygame.Color('red'), i_rect)
                                                        for i_rect in grid]
                game_end = 1

    # конец игры
    if game_end == 1:
        game_end = 0
        set_record(hi_score, game_score)
        anim_speed = 100
        level_game = 1
        game_score = 0
        speed_game = 5
        plus_score = 10
        scores = 0
        game_over()

    # движение машинок + анимация дороги(движение бортов)
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        for j in range(7):
            enemy_car[j].y += 1
            enemy_car2[j].y += 1
            enemy_car3[j].y += 1
            if enemy_car[j].y > 23:
                enemy_car[j].y = -3
                game_score += plus_score
                if enemy_car[j].x < 5:
                    line = int(random.choice(side_generation))
                    for k in range(7):
                        enemy_car[k].x += line
                else:
                    if enemy_car[j].x > 4:
                        line = int(random.choice(side_generation))
                        for k in range(7):
                            enemy_car[k].x -= line
            elif enemy_car2[j].y > 23:
                enemy_car2[j].y = -3
                game_score += plus_score
                if enemy_car2[j].x < 5:
                    line = int(random.choice(side_generation))
                    for k in range(7):
                        enemy_car2[k].x += line
                else:
                    if enemy_car2[j].x > 4:
                        line = int(random.choice(side_generation))
                        for k in range(7):
                            enemy_car2[k].x -= line
            elif enemy_car3[j].y > 23:
                enemy_car3[j].y = -3
                game_score += plus_score
                if enemy_car3[j].x < 5:
                    line = int(random.choice(side_generation))
                    for k in range(7):
                        enemy_car3[k].x += line
                else:
                    if enemy_car3[j].x > 4:
                        line = int(random.choice(side_generation))
                        for k in range(7):
                            enemy_car3[k].x -= line
        for i in range(28):
            figure_borders[i].y += 1
            if figure_borders[i].y > H:
                figure_borders[i].y = 0

    # отрисовка сетки
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # отрисовка игровой машинки
    for i in range(7):
        figure_rect.x = figure_car[i].x * size_tile
        figure_rect.y = figure_car[i].y * size_tile
        pygame.draw.rect(game_sc, pygame.Color('black'), figure_rect)

    # отрисовка NPS машинок
    for j in range(7):
        figure_rect.x = enemy_car[j].x * size_tile
        figure_rect.y = enemy_car[j].y * size_tile
        pygame.draw.rect(game_sc, pygame.Color('black'), figure_rect)
        figure_rect.x = enemy_car2[j].x * size_tile
        figure_rect.y = enemy_car2[j].y * size_tile
        pygame.draw.rect(game_sc, pygame.Color('black'), figure_rect)
        figure_rect.x = enemy_car3[j].x * size_tile
        figure_rect.y = enemy_car3[j].y * size_tile
        pygame.draw.rect(game_sc, pygame.Color('black'), figure_rect)

    # отрисовка бортов
    for i in range(28):
        figure_rect.x = figure_borders[i].x * size_tile
        figure_rect.y = figure_borders[i].y * size_tile
        pygame.draw.rect(game_sc, pygame.Color('black'), figure_rect)

    # вывод дынных игры
    sc.blit(title_races, (330, 10))
    sc.blit(title_score, (350, 90))
    sc.blit(myfont1.render(str(game_score), True, pygame.Color('red')),
                                                                (350, 130))
    sc.blit(title_hi_score, (350, 220))
    sc.blit(myfont1.render(str(hi_score), True, pygame.Color('red')),
                                                            (360, 260))
    sc.blit(title_level, (350, 400))
    sc.blit(myfont1.render(str(level_game), True, pygame.Color('green')),
                                                                (360, 440))
    sc.blit(title_speed, (350, 530))
    sc.blit(myfont1.render(str(speed_game), True, pygame.Color('green')),
                                                                (360, 570))

    pygame.display.flip()
    clock.tick(game_fps)
