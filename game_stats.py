class GameStats():
    """外星人入侵的跟踪统计"""
    
    def __init__(self, ai_game):
        """初始化数据"""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # Start Alien Invasion in an active state.
        self.game_active = False

        # High score should never be reset.
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