class Settings():
    """存储《外星人入侵》所有设置类"""

    def __init__(self):
        """初始化游戏设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (204, 232, 207)

        """飞船设置"""
        # self.ship_speed_factor = 1.5
        self.ship_limit = 3
        """子弹设置"""
        # self.bullet_speed_factor = 3
        # 测试子弹时候可增加子弹宽度为300
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 9

        """外星人设置"""
        # self.alien_speed_factor = 1
        # 外星人撞到屏幕右边后向下移动再向左移动
        self.fleet_drop_speed = 10
        # fleet_direction表示1向右移动，-1表示向左移动
        # self.fleet_direction = 1
        # 以什么速度加快游戏
        self.speedup_scale = 1.3
        # 外星人点数提高速度
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的变量"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleeet_direction为1表示向右，-1表示向左
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
