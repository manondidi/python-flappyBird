#coding=utf-8
import pygame  # 导入pygame库
from pygame.locals import *  # 导入pygame库中的一些常量
import sys
from Bird import *
import random
import ResourceLoader
from Floor import Floor
from Pipe import Pipe

SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FPS = 30
HORIZONTAL_DISTANCE = SCREEN_WIDTH / 2
VERTICAL_DISTANCE = 120
COUNT = 3
OFFSET_X = SCREEN_WIDTH
OFFSET_Y = 80
window_size = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

point = 0
last_pipe = None


def main():
    global CLOCK, SCREEN, bird, floor, point, last_pipe, point_sound
    pygame.init()  # 初始化pygame
    pygame.mixer.init()
    point_sound = ResourceLoader.get_sound("point.wav")
    wing_sound = ResourceLoader.get_sound("wing.wav")
    die_sound = ResourceLoader.get_sound("die.wav")
    CLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  # 初始化一个用于显示的窗口
    pygame.display.set_caption('flappyBird')  # 设置窗口标题.

    bird = Bird(window_size, wing_sound, die_sound)
    floor = Floor(window_size)
    background = ResourceLoader.get_image("background-day.png")
    message = ResourceLoader.get_image("message.png")
    message_rect = (message.get_rect(centerx=SCREEN_WIDTH / 2, centery=SCREEN_HEIGHT / 2))
    reset()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    if not bird.isDie:
                        bird.fly()
                    else:
                        reset()
        if not bird.isDie:
            bird.update()
            floor.update()
        SCREEN.blit(background, (0, 0))
        if not bird.begin_fly and not bird.isDie:
            SCREEN.blit(message, (message_rect.x, message_rect.y))
        else:
            for i in range(COUNT):
                center_y = make_center_y()
                pipe_top = pipes_top[i]
                pipe_botom = pipes_botom[i]
                if not bird.isDie:
                    pipe_top.update(center_y)
                    pipe_botom.update(center_y)
                SCREEN.blit(pipe_top.image, (pipe_top.rect.x, pipe_top.rect.y))
                SCREEN.blit(pipe_botom.image, (pipe_botom.rect.x, pipe_botom.rect.y))

        SCREEN.blit(floor.image, (floor.rect.x, floor.rect.y))
        SCREEN.blit(bird.get_bird_image(), (bird.rect.x, bird.rect.y))
        if bird.isDie:
            game_over = ResourceLoader.get_image("gameover.png")
            SCREEN.blit(game_over, (
                (SCREEN_WIDTH - game_over.get_rect().width) / 2, (SCREEN_HEIGHT - game_over.get_rect().height) / 2))
        if bird.begin_fly:
            show_point()
            if check_conlision():
                bird.die()

        pygame.display.flip()
        CLOCK.tick(FPS)


def show_point():
    global last_pipe, point
    if not bird.isDie and bird.begin_fly:
        arr = list(filter(lambda pipe:
                          bird.rect.x > (pipe.rect.x + pipe.rect.width) > 0,
                          pipes_botom))
        if arr:
            if last_pipe != arr[0]:
                point += 1
                last_pipe = arr[0]
                point_sound.play()

    point_str = str(point)
    num_image_list = []
    for num in point_str:
        num_image_list.append(ResourceLoader.get_image(ResourceLoader.NUMBER_IMAGES[int(num)]))
    numbers_width = len(point_str) * ResourceLoader.get_image(ResourceLoader.NUMBER_IMAGES[0]).get_rect().width
    first_num_x = (SCREEN_WIDTH - numbers_width) / 2

    for i in range(len(num_image_list)):
        SCREEN.blit(num_image_list[i], (first_num_x + i * numbers_width / len(point_str), 50))


def reset():
    global sprite_group, pipes_top, pipes_botom, point
    bird.reset()
    pipes_top = []
    pipes_botom = []
    Pipe.top_index = 0
    Pipe.bottom_index = 0
    point = 0

    for i in range(COUNT):
        center_y = make_center_y()
        pipes_top.append(Pipe(OFFSET_X, OFFSET_Y, window_size, True, HORIZONTAL_DISTANCE, VERTICAL_DISTANCE, center_y))
        pipes_botom.append(
            Pipe(OFFSET_X, OFFSET_Y, window_size, False, HORIZONTAL_DISTANCE, VERTICAL_DISTANCE, center_y))
    sprite_group = []
    sprite_group.append(floor)
    sprite_group.extend(pipes_top)
    sprite_group.extend(pipes_botom)


def check_conlision():
    return pygame.sprite.spritecollide(bird, sprite_group, False, pygame.sprite.collide_mask)


def make_center_y():
    center_y = random.randint(bird.rect.y - 80, bird.rect.y + 80)
    if center_y - VERTICAL_DISTANCE / 2 < 120:
        center_y = 120 + random.randint(0, 40)
    elif center_y + VERTICAL_DISTANCE / 2 > SCREEN_HEIGHT - 120 - floor.rect.height:
        center_y = SCREEN_HEIGHT - 120 - floor.rect.height - random.randint(0, 40)

    return center_y


if __name__ == "__main__":
    main()
