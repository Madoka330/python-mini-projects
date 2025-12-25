import pygame

from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import AlienInvasion

class Bullet(Sprite):
    """管理飞船所发射的子弹类"""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        """在飞船的当前位置创建一个子弹对象"""

        super().__init__()  # 初始化父类
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # 在 (0, 0) 处创建一个表示子弹的矩形，在设置其正确位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 子弹位置
        self.y = float(self.rect.y)

    def update(self) -> None:
        """向上移动子弹"""

        # 更新子弹的准确位置
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        """在屏幕上绘制子弹"""

        pygame.draw.rect(self.screen, self.color, self.rect)