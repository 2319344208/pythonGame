import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import *
class AlienInvasion:
    def __init__(self):
        """管理游戏资源和行为的类."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")


        #创建类存储数据,
        #  创建记分板.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # 创建飞船
        self.ship = Ship(self)
        # 创建子弹 外星人和 星星的 编组
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()


        # 开始游戏按钮.
        self.play_button = Button(self, "Play")
    def run_game(self):
      """开始为游戏主循环"""
      self.create_stars(self.stars, self.screen.get_width(), self.screen.get_height(), 100, 100)
      while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """点击开始游戏按钮."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """按键事件"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # 添加
        elif event.key==pygame.K_UP:
            self.ship.moving_up=True
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=True

    def _check_keyup_events(self, event):
        """松键事件."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key==pygame.K_UP:
            self.ship.moving_up=False
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=False
    def _fire_bullet(self):
        """创建子弹让其加入编组bullets中."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹位置，同时让删除消失子弹"""
        # 更新子弹位置.
        self.bullets.update()

        # 删除消失子弹.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """子弹撞击外星人处理方法."""
        # 删除碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹编组并且重新创建一个外星人群.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提升等级.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """检查外星人群是否在边缘位置若是则更新位置"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检查飞船是否与外星人碰撞.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查外星人中是否有在屏幕底部的.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查外星人中是否有在屏幕底部的."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """飞船被外星人碰撞后的处理方法."""
        if self.stats.ships_left > 0:
            #飞船被外星人袭击.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 删除所有的子弹和外星人.
            self.aliens.empty()
            self.bullets.empty()

            # 创建新的外星人并且让飞船回到中心.
            self._create_fleet()
            self.ship.center_ship()

            # 暂定0.5s.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """创建外星人群."""
        # 创建外星人，并确定一行可以容纳多少个外星人.
        # 每个外星人之间的间距等于一个外星人的宽度.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 确定外星人的行数.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建完整的外星人群.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """在指定行创建一个外星人"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_star(self,stars, star_right_coordinate, random_x_space, star_bottom_coordinate, random_y_space):
        star = Star()

        # 新增星星左坐标为前一星星右坐标加随机横间距
        star.rect.x = star_right_coordinate + random_x_space

        # 每行星星上方留出适当空间
        star.rect.y = star_bottom_coordinate + random_y_space
        stars.add(star)

    def create_stars(self,stars, screen_width, screen_height, max_x_space, max_y_space):
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
                self.create_star(stars, star_right_coordinate, random_x_space, star_bottom_coordinate, random_y_space)

                # 重置前一星星右坐标和随机横间距
                star_right_coordinate = star_right_coordinate + star.rect.width + random_x_space
                random_x_space = randint(1, max_x_space)

            # 重置前一星星右坐标、前行星星底坐标和随机纵间距
            star_right_coordinate = 0
            star_bottom_coordinate = star_bottom_coordinate + star.rect.height + random_y_space
            random_y_space = randint(1, max_y_space)

    def _check_fleet_edges(self):
        """如果任何外星人达到边界则重新定位外星人群的位置"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """整个外星人群下移，同时改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # 显示分数信息.
        self.sb.show_score()

        # 如果游戏属于非活动状态则画出开始游戏按钮.
        if  not self.stats.game_active :
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # 开始游戏.
    ai = AlienInvasion()
    ai.run_game()
