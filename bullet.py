import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управлением снарядами корабля"""

    def __init__(self, ai_game):
        # Создаёт объект снарядов в текущей позиции корабля
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.color = self.setting.bullet_color

        # Создание снаряда в позиции (0, 0) и назначение правильной позиции
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width,
                                self.setting.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        # Перемещает снаряд вверх по экрану
        self.y -= self.setting.bullet_spead
        # Обновление позиции снаряда
        self.rect.y = self.y

    def draw_bullet(self):
        # Вывод снаряда на экран
        pygame.draw.rect(self.screen, self.color, self.rect)

