#coding=utf-8
import pygame
from pygame import sprite
import ResourceLoader


class Bird(sprite.Sprite):
    SPEED = 10
    MAX_FLY_HEIGHT = 70
    flying = True
    MAX_UP_ANGLE = 20
    MAX_DOWN_ANGLE = -30

    def __init__(self, window_size, wing_sound, die_sound):
        super().__init__()
        self.images = ResourceLoader.get_images(
            ["bluebird-midflap.png", "bluebird-upflap.png", "bluebird-downflap.png"])
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.currentY = self.rect.y
        self.status = 0
        self.window_size = window_size
        self.isDie = False
        self.begin_fly = False
        self.wing_sound = wing_sound
        self.die_sound = die_sound
        self.reset()

    def die(self):
        self.isDie = True
        self.begin_fly = False
        self.die_sound.play()

    def reset(self):
        self.rect.x = 40
        self.rect.y = 290
        self.isDie = False
        self.begin_fly = False

    def fly(self):
        self.begin_fly = True
        self.flying = True
        self.currentY = self.rect.y
        self.wing_sound.play()

    def update(self):
        if self.begin_fly:
            if self.flying and self.rect.y > self.currentY - self.MAX_FLY_HEIGHT \
                    and self.rect.y > 0:

                self.rect.y -= self.SPEED  # 向上
            elif self.rect.y < self.window_size.height:
                self.flying = False
                self.rect.y += self.SPEED * 0.6  # 向下

    count = 0

    def get_bird_image(self):
        self.count += 1
        if self.count % 5 == 0 and not self.isDie:
            self.image = self.get_next_status()
        return self.get_bird_rotate()

    def get_bird_rotate(self):
        angle = 0
        if self.begin_fly:
            if self.flying:
                distance = self.currentY - self.MAX_FLY_HEIGHT
                if distance == 0:
                    angle = 20
                else:
                    angle = self.rect.y / distance * self.MAX_UP_ANGLE
                    if angle > 20:
                        angle = 20
            else:
                angle = self.MAX_DOWN_ANGLE

        return pygame.transform.rotate(self.image, angle)

    def get_next_status(self):
        self.status += 1
        image = self.images[self.status % 3]
        return image
