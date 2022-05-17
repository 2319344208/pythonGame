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
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")


        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()


        # Make the Play button.
        self.play_button = Button(self, "Play")
    def run_game(self):
      """Start the main loop for the game."""
      self.create_stars(self.stars, self.screen.get_width(), self.screen.get_height(), 100, 100)
      while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
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
        """Start a new game when the player clicks Play."""
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
        """Respond to keypresses."""
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
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key==pygame.K_UP:
            self.ship.moving_up=False
        elif event.key==pygame.K_DOWN:
            self.ship.moving_down=False
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
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
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

# def run_game():
#     # pygame进行初始化,设置参数,和屏幕对象
#     pygame.init()
#     ai_settings = Settings()
#     screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#     # screen = pygame.display.set_mode(
#     #     (ai_settings.screen_width, ai_settings.screen_height))
#     pygame.display.set_caption("Alien Invasion")
#
#     # Make the Play button.
#     play_button = Button(ai_settings, screen, "Play")
#
#     # Create an instance to store game statistics.
#     stats = GameStats(ai_settings)
#     sb = Scoreboard(ai_settings, screen, stats)
#
#     # 设置背景颜色.
#     bg_color = (230, 230, 230)
#
#     # 创建一艘飞船.
#     ship = Ship(ai_settings, screen)
#     # 定义子弹数组.
#     bullets = Group()
#     aliens = Group()
#
#     # Create the fleet of aliens.
#     gf.create_fleet(ai_settings, screen, ship, aliens)
#
#     #开始游戏主循环.
#     while True:
#         gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
#                         aliens, bullets)
#         if stats.game_active:
#             ship.update()
#             gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
#                               bullets)
#             gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
#                              bullets)
#         gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
#                          bullets, play_button)
#
# run_game()
