import pygame
from pygame import sprite
import ResourceLoader


class Floor(sprite.Sprite):
    SPEED = 6

    def __init__(self, window_size):
        super().__init__()
        self.window_size = window_size
        self.image = ResourceLoader.get_image("base.png")
        self.rect = self.image.get_rect()
        self.rect.y = window_size.height - self.rect.height

    def update(self):
        out = self.rect.width - self.window_size.width  # 图片超出屏幕部分
        if abs(self.rect.x) >= out:
            self.rect.x = 0
        else:
            self.rect.x -= self.SPEED
