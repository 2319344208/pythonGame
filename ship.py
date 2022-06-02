from tkinter import Image

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_game):
        """初始化船并且设置其初始位置."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # 飞船翻转标志为False时才翻转
        self.turn=False

        # 加载飞船图片并获得其外接矩形.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #开始每个新船在屏幕底部的中心.
        # self.rect.midbottom = self.screen_rect.midbottom
        # 出现在左边
        self.rect.midleft = self.screen_rect.midleft

        # 存储飞船的位置.
        self.x = float(self.rect.x)
        # 添加功能
        self.y=float(self.screen_rect.height/2)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up=False
        self.moving_down=False
    def update(self):
        """如果对应移动标志为ture则对应的移动飞船."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 添加部分
        if self.moving_down and self.rect.bottom <self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_up and self.rect.top >0:
            self.y -= self.settings.ship_speed

        # 更新船的位置.
        self.rect.x = self.x
        self.rect.y=self.y


    def blitme(self):
        """在屏幕中绘制出船的图片."""
        if(self.turn==False):
          self.image=pygame.transform.rotate(self.image,-90)
          self.turn=True
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕中心."""
        self.rect.midleft = self.screen_rect.midleft
        self.x = float(self.rect.x)
        self.y=float(self.screen_rect.height/2)
