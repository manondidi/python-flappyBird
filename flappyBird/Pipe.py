#coding=utf-8
import pygame
from pygame import sprite
import ResourceLoader


class Pipe(sprite.Sprite):
    SPEED = 6
    top_index = 0
    bottom_index = 0

    def __init__(self, offset_x, offset_y, window_size, reverse, horizontal_distance, vertical_distance, center_y):
        super().__init__()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.window_size = window_size
        self.image = ResourceLoader.get_image("pipe-green.png")
        self.rect = self.image.get_rect()
        self.reverse = reverse
        self.horizontal_distance = horizontal_distance
        self.vertical_distance = vertical_distance
        self.center_y = center_y
        if reverse:
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect.x = Pipe.top_index * (self.rect.width + self.horizontal_distance) + offset_x
            self.rect.y = center_y - self.rect.height - self.vertical_distance / 2
            Pipe.top_index += 1
        else:
            self.rect.x = Pipe.bottom_index * (self.rect.width + self.horizontal_distance) + offset_x
            self.rect.y = center_y + self.vertical_distance - self.vertical_distance / 2
            Pipe.bottom_index += 1

    def update(self, center_y):
        right = self.rect.x + self.rect.width
        if right < 0:
            self.rect.x = self.offset_x + self.horizontal_distance + self.rect.width * 2
            if self.reverse:
                self.rect.y = center_y - self.rect.height - self.vertical_distance / 2
            else:
                self.rect.y = center_y + self.vertical_distance / 2
        else:
            self.rect.x -= self.SPEED
