import pygame
import sys
from setting import Setting
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Класс для управлениями ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы"""
        pygame.init()
        self.setting = Setting()
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        pygame.display.set_caption("Star Wars")
        pygame.display.set_icon(self.setting.icon)
        self.ship = Ship(Setting)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keydown_events(self, event):
        # Реагирует на нажатие клавиш
        if event.key == pygame.K_RIGHT:
            # Переместить корабль в право
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Переместить корабль в лево
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        # Создаёт новый снаряд и включает его в группу bullets
        if len(self.bullets) < self.setting.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keyup_event(self, event):
        # Реагирует на отпускание клавиш
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _create_fleet(self):
        # Создание флота вторжения
        # Вычисления длинны ряда
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.setting.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        # Вычисление высоты ряда
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Создание первого ряда пришельцев
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        # Реагирует на достижение пришельцем края экрана
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # Опускает весь флот и меняет его направление
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _update_screen(self):
        """При каждом проходе цикла перерисовывается экран"""
        self.screen.fill(self.setting.bg_color)
        self.ship.update()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        """Отображение последнего экрана"""
        pygame.display.flip()

    def _update_bullet(self):
        # Удаление старых снарядов и вывод на экран новых
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_aliens(self):
        # Обновление позиции всех пришельцев на флоте
        self._check_fleet_edges()
        self.aliens.update()

    def run_game(self):
        """Запуск основного цикла игры"""
        self._create_fleet()
        while True:
            self._check_events()
            self._update_screen()
            self._update_bullet()
            self._update_aliens()
