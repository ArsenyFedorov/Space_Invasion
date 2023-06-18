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

        """Загружаем изображение корабля и получаем прямоугольник"""
        self.images = pygame.image.load("Picture/ship.png")
        self.rect = self.images.get_rect()
        """Каждый новый корабль появляется у нижнего края экрана """
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.images, self.rect)

