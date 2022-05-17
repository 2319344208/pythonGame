import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_game):
        """初始化船并且设置其初始位置."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        # self.rect.midbottom = self.screen_rect.midbottom
        # 出现在左边
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        # 添加功能
        self.y=float(self.screen_rect.bottom-self.rect.height)

        # Movement flags
        self.moving_right = False
        self.moving_left = False
        # 本人添加功能
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
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y=float(self.screen_rect.bottom-self.rect.height)
