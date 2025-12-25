import sys
import pygame

from bullet import Bullet
from settings import Settings
from ship import Ship  
from typing import cast        # 用 cast 声明变量类型
  
class AlienInvasion:
    """管理游戏资源和行为的类"""
    
    def __init__(self) -> None:
        """初始化游戏并创建游戏资源"""

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_witdh, self.settings.screen_height)
        )

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() 

    def run_game(self) -> None:
        """开始游戏的主循环"""
 
        while True:
            self._check_event()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_event(self) -> None:
        """响应键盘和鼠标事件"""

        for event in pygame.event.get():
            # 退出
            if event.type == pygame.QUIT:
                sys.exit()
            # 键盘按下
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            # 键盘释放
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keydown_event(self, event: pygame.event.Event) -> None:
        """响应按下"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True       
        elif event.key == pygame.K_q:
            sys.exit() 
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event: pygame.event.Event) -> None:
        """响应释放"""

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self) -> None:
        """创建一颗子弹，并将其加入编组 bullets"""

        # 最多允许 3 枚子弹
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self) -> None:
        """更新子弹的位置并删除已经消失的子弹"""

        self.bullets.update()

        # 删除已经消失的子弹（Python 遍历数组的时候要求数组不变，所以这里遍历其拷贝）
        for bullet in self.bullets.copy(): 
            bullet = cast(Bullet, bullet)
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
    
    def _update_screen(self) -> None:
        """更新屏幕上的图片，并切换到新屏幕"""

        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites(): 
            bullet = cast(Bullet, bullet)
            bullet.draw_bullet()
        self.ship.blitme()
        pygame.display.flip()

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()