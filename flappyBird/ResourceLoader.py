import os
import pygame  # 导入pygame库

CURRENT_PATH = os.path.dirname(__file__)
RESOURCE_PATH = os.path.join(CURRENT_PATH, 'resources')
IMAGES_PATH = os.path.join(RESOURCE_PATH, 'images')
SOUNDS_PATH = os.path.join(RESOURCE_PATH, 'sounds')

NUMBER_IMAGES = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png"]


def get_image(image_name):
    return pygame.image.load(os.path.join(IMAGES_PATH, image_name)).convert_alpha()


def get_images(image_name_arr):
    return list(map(get_image, image_name_arr))


def get_sound(sound_name):
    return pygame.mixer.Sound(os.path.join(SOUNDS_PATH, sound_name))


def get_sounds(sound_name_arr):
    return list(map(get_sound, sound_name_arr))
