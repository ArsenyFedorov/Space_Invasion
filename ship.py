import pygame
from setting import Setting

class Ship:
    """Класс для управления кораблём"""

    def __init__(self, ai_game):
        """Инициализирует корабль и задаёт изначальную позицию"""
        self.setting = ai_game()
        self.screen = pygame.display.set_mode(
            (self.setting.screen_width, self.setting.screen_height))
        self.screen_rect = self.screen.get_rect()
        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        """Загружаем изображение корабля и получаем прямоугольник"""
        self.images = pygame.image.load("Picture/ship.png")
        self.rect = self.images.get_rect()
        """Каждый новый корабль появляется у нижнего края экрана """
        self.rect.midbottom = self.screen_rect.midbottom
        # Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.images, self.rect)

    def update(self):
        # Обновление позиции корабля с учётом значение флаг
        # Обновление атрибута х не rect
        if self.moving_right:
            self.x += self.setting.ship_speed
        if self.moving_left:
            self.x -= self.setting.ship_speed
        # Обновление атрибута rect на основе self.x
        self.rect.x = self.x


