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
        self.ship_limit = 3
        # Настройка снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)
        self.bullet_allowed = 3
        # Настройка НЛО
        self.alien_points = 50
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        # Ускорение игры
        self.speedup_scale = 1.2
        self.initialize_dinamic_setting()
        # Увиличение стоимости пришельца
        self.score_scale = 1.5

    def initialize_dinamic_setting(self):
        """Инициализирует настройки изминяющиеся в ходе игры"""
        self.ship_speed = 1.5
        self.bullet_spead = 3.0
        self.alien_speed = 0.2
        self.fleet_direction = 1

    def increase_speed(self):
        """Увиличивает настройки скорости"""
        self.ship_speed *= self.speedup_scale
        self.bullet_spead *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

