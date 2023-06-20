import pygame


class Setting:
    """Класс для хранения настроек игры"""

    def __init__(self):
        """Инициализирует настройки игры"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.icon = pygame.image.load("Picture/UFO.png")
        # Настройки корабля
        self.ship_speed = 2
        # Настройка снаряда
        self.bullet_spead = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (51, 255, 255)
        self.bullet_allowed = 3
        # Настройка НЛО
        self.alien_speed = 0.2
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

