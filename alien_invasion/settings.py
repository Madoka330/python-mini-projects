class Settings:
    """游戏相关设置"""

    def __init__(self) -> None:
        """初始化游戏设置"""
        
        # 屏幕设置
        self.screen_witdh = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 3
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        # 外星人设置
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1    # 1 表示向右，-1 表示向左  