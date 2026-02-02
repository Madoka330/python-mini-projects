import sys
from time import sleep

import pygame

from bullet import Bullet
from settings import Settings
from game_stats import GameStats
from ship import Ship  
from alien import Alien
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

        # 创建一个用于储存游戏统计信息的实例
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() 
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()

        # 游戏启动后处于活动状态
        self.game_active = True

    def run_game(self) -> None:
        """开始游戏的主循环"""
 
        while True:
            self._check_event()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien()
                
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
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""

        # 检查是否有子弹击中了外星人，如果击中了，就删除对应的外星人和子弹
        collisions = pygame.sprite.groupcollide(
            groupa=self.bullets, groupb=self.aliens, dokilla=True, dokillb=True
        )

        if not self.aliens:
            # 删除现有的子弹并且创建一个新的外星舰队
            self._create_fleet()
            self.bullets.empty()

    def _create_fleet(self) -> None:
        """创建一个外星舰队"""

        # 创建一个外星人再不断添加，直到没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        x_pos, y_pos = alien_width, alien_height

        while y_pos + 3 * alien_height < self.settings.screen_height:
            while x_pos + 2 * alien_width < self.settings.screen_witdh:
                self._create_alien(x_pos, y_pos)
                x_pos += 2 * alien_width 
            x_pos = alien_width
            y_pos += 2 * alien_width           


    def  _create_alien(self, x_pos: int, y_pos: int) -> None:
        """创建一个外星人"""

        new_alien = Alien(self)
        new_alien.x = x_pos
        new_alien.rect.x = x_pos
        new_alien.rect.y = y_pos
        self.aliens.add(new_alien)

    def _update_alien(self) -> None:
        """更新外星舰队中外星人的位置"""

        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检测是否有外星人到达屏幕的下边缘
        self._check_aliens_bottom()

    def _check_fleet_edges(self) -> None:
        """在有外星人到达边缘时采取相应的措施"""

        for alien in self.aliens.sprites():
            alien = cast(Alien, alien)
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        """将整个外星舰队向下移动，并改变它们的方向"""

        for alien in self.aliens.sprites():
            alien = cast(Alien, alien)
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""

        if self.stats.ships_left > 0:
            # 将 ships_left 减 1
            self.stats.ships_left -= 1

            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()

            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        """检测是否有外星人到达了屏幕的下边缘"""

        for alien in self.aliens.sprites():
            alien = cast(Alien, alien)
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到了一样进行处理
                self._ship_hit()
                break


    def _update_screen(self) -> None:
        """更新屏幕上的图片，并切换到新屏幕"""

        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites(): 
            bullet = cast(Bullet, bullet)
            bullet.draw_bullet()
        self.ship.blitme() 
        self.aliens.draw(self.screen)  # 适用于直接按照图像绘制
        pygame.display.flip()

if __name__ == "__main__":
    AlienInvasion().run_game()