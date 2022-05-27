class GameStats():
    """外星人入侵的跟踪统计"""
    def __init__(self, ai_game):
        """初始化数据"""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # 游戏活动初始状态为False.
        self.game_active = False

        # 不能重置最高分.
        self.high_score =self.get_high_score()
        
    def reset_stats(self):
        """根据游戏改变初始化数据"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
    def get_high_score(self):
        with open('score.txt',encoding='utf-8') as file:
            score=file.read()
            if score=="":
                high_score=0
            else:
                high_score=int(score)
        return high_score