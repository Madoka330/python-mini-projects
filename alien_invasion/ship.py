import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import AlienInvasion

class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game: "AlienInvasion") -> None: 
        """初始化飞船并设置其初始位置"""

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load("alien_invasion\images\ship.bmp")
        self.rect = self.image.get_rect()
        
        # 每艘飞船都放在屏幕底部的正中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 飞船位置
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self) -> None:
        """根据移动标志调整飞船的位置"""

        # 更新飞船属性的 x 而不是外接矩形的 x
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        # 根据 self.x 更新 rect 对象
        self.rect.x = self.x

    def blitme(self) -> None:
        """在指定位置绘制飞船"""

        self.screen.blit(self.image, self.rect)
