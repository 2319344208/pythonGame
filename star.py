import sys
import pygame
from pygame.sprite import Sprite, Group
from random import randint


class Star(Sprite):
    def __init__(self):
        super().__init__()
        # 加载星星图像
        self.image = pygame.image.load('images/star.png')
        self.rect = self.image.get_rect()






