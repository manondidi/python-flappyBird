import pygame  # 导入pygame库
from pygame.locals import *  # 导入pygame库中的一些常量
import sys
import random
from enum import Enum

# 定义窗口的分辨率
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

COL = 16 * 2
ROW = 12 * 2
CELL_WIDTH = SCREEN_WIDTH / COL
CELL_HEIGHT = SCREEN_HEIGHT / ROW

WHITE = (255, 255, 255)
FOOD_COLOR = (255, 0, 0)
SNACK_HEAD_COLOR = (0, 230, 0)
SNACK_BODY_COLOR = (0, 255, 0)
CENTER_POSITION = [COL // 2, ROW // 2]

pygame.init()  # 初始化pygame
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])  # 初始化一个用于显示的窗口
pygame.display.set_caption('贪食蛇')  # 设置窗口标题.

head_position = CENTER_POSITION
body_position_arr = [[head_position[0], head_position[1] + 1]]
food_position = []

clock = pygame.time.Clock()


def make_food():
    global food_position
    food_position = make_food_position()


def make_food_position():
    x = random.randint(1, COL-1)
    y = random.randint(1, ROW-1)
    food_position_local = [x, y]
    if not check_same_position(food_position_local, head_position) and not list(
            filter(lambda position: check_same_position(food_position_local, position), body_position_arr)):
        return food_position_local
    else:
        return make_food_position()


def check_same_position(position, other_position):
    return (position and other_position) and position[0] == other_position[0] and position[1] == other_position[1]


def check_head_food(): 
    return check_same_position(head_position, food_position)


def check_head_body():
    return list(filter(lambda position: check_same_position(head_position, position), body_position_arr))


def check_head_window():
    return head_position[0] < 0 or head_position[0] >= COL or head_position[1] < 0 or head_position[1] >= ROW


def draw_rect(color, col, row):
    pygame.draw.rect(screen, color, pygame.Rect(col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))


class Dirction(Enum):
    left = 0,
    right = 1,
    up = 2,
    down = 3


dirction = Dirction.left


def make_dirction(dirc):
    global dirction
    if dirction == Dirction.left and dirc != Dirction.right \
            or dirction == Dirction.right and dirc != Dirction.left \
            or dirction == Dirction.up and dirc != Dirction.down \
            or dirction == Dirction.down and dirc != Dirction.up:
        dirction = dirc


def move():
    global food_position
    body_position_arr.insert(0, head_position.copy())
    if dirction == Dirction.left:
        head_position[0] -= 1
    if dirction == Dirction.right:
        head_position[0] += 1
    if dirction == Dirction.up:
        head_position[1] -= 1
    if dirction == Dirction.down:
        head_position[1] += 1
    if check_head_food():
        food_position = None
    else:
        body_position_arr.pop()

    if check_head_body() or check_head_window():
        sys.exit()



def main():
    global food_position
    global dirction
    # 事件循环(main loop)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    make_dirction(Dirction.left)
                if event.key == K_RIGHT:
                    make_dirction(Dirction.right)
                if event.key == K_UP:
                    make_dirction(Dirction.up)
                if event.key == K_DOWN:
                    make_dirction(Dirction.down)
        screen.fill(WHITE)
        move()
        if not food_position:
            make_food()
        draw_rect(FOOD_COLOR, food_position[0], food_position[1])

        draw_rect(SNACK_HEAD_COLOR, CENTER_POSITION[0], CENTER_POSITION[1])
        for body in body_position_arr:
            draw_rect(SNACK_BODY_COLOR, body[0], body[1])
        pygame.display.flip()
        clock.tick(6)


if __name__ == "__main__":
    main()
