import pygame
import sys
from setting import Setting
from ship import Ship


class AlienInvasion:
    """Класс для управлениями ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы"""
        pygame.init()
        self.setting = Setting()
        self.screen = pygame.display.set_mode(
            (self.setting.screen_width, self.setting.screen_height))
        pygame.display.set_caption("Star Wars")
        pygame.display.set_icon(self.setting.icon)
        self.ship = Ship(Setting)

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Переместить корабль в право
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    # Переместить корабль в лево
                    self.ship.moving_left = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_screen(self):
        """При каждом проходе цикла перерисовывается экран"""
        self.screen.fill(self.setting.bg_color)
        self.ship.update()
        self.ship.blitme()

        """Отображение последнего экрана"""
        pygame.display.flip()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            self._update_screen()


