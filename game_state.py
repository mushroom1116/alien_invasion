class GameState():
    """跟踪游戏统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_state()
        # 游戏刚启动时处于活跃态
        self.game_active = False
        # 任何情况下都不应该重最高分
        self.high_score = 0

    def reset_state(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
