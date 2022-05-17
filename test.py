# -*- coding: utf-8 -*-

import sys
import pygame

from pygame.sprite import Group
from random import randint


class Star(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # 加载星星图像
        self.image = pygame.image.load('images/star.png')
        self.rect = self.image.get_rect()


def create_star(stars, star_right_coordinate, random_x_space, star_bottom_coordinate, random_y_space):
    star = Star()

    # 新增星星左坐标为前一星星右坐标加随机横间距
    star.rect.x = star_right_coordinate + random_x_space

    # 每行星星上方留出适当空间
    star.rect.y = star_bottom_coordinate + random_y_space
    stars.add(star)


def create_stars(stars, screen_width, screen_height, max_x_space, max_y_space):
    star = Star()

    # 记录前一星星右坐标
    star_right_coordinate = 0

    # 记录前行星星底坐标
    star_bottom_coordinate = 0

    # 增加随机横间距
    random_x_space = randint(1, max_x_space)

    # 增加随机行间距
    random_y_space = randint(1, max_y_space)

    # 屏幕纵向空间足够时循环创建整行星星
    while star_bottom_coordinate + star.rect.height + random_y_space < screen_height:

        # 屏幕横向空间足够时循环创建单个星星
        while star_right_coordinate + star.rect.width + random_x_space < screen_width:
            create_star(stars, star_right_coordinate, random_x_space, star_bottom_coordinate, random_y_space)

            # 重置前一星星右坐标和随机横间距
            star_right_coordinate = star_right_coordinate + star.rect.width + random_x_space
            random_x_space = randint(1, max_x_space)

        # 重置前一星星右坐标、前行星星底坐标和随机纵间距
        star_right_coordinate = 0
        star_bottom_coordinate = star_bottom_coordinate + star.rect.height + random_y_space
        random_y_space = randint(1, max_y_space)


def run_game():
    pygame.init()

    # 设置屏幕参数
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    bg_color = (230, 230, 230)

    # 设置星星间距最大值
    max_x_space = 100
    max_y_space = 100

    # 创建用于存储星星的编组
    stars = Group()

    # 创建全屏幕星星
    create_stars(stars, screen_width, screen_height, max_x_space, max_y_space)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bg_color)
        stars.draw(screen)
        pygame.display.flip()


run_game()
