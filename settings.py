class Settings():
    """该类用于设置外星人游戏的相关参数."""

    def __init__(self):
        """游戏参数设置初始化."""
        # 屏幕参数设置.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船参数设置.
        self.ship_limit = 3
        # 子弹参数设置.
        self.bullet_width = 8
        self.bullet_height = 10
        # 子弹颜色
        self.bullet_color = 60, 60, 60
        # 限制子弹数量
        self.bullets_allowed = 20

        # 外星人参数设置
        self.fleet_drop_speed=10.0

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化设置."""
        self.ship_speed = 4.0
        self.bullet_speed = 6.0
        self.alien_speed = 1.0


        # fleet_direction 1 代表下; -1 代表上.
        self.fleet_direction = 1

        # 一个外星人分数50
        self.alien_points = 50
    def increase_speed(self):
        """提高速度."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
