import pygame
import sys
from time import sleep

from setting import Setting
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_status import GameStatus
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Класс для управлениями ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы"""
        pygame.init()
        self.setting = Setting()
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        pygame.display.set_caption("Star Wars")
        pygame.display.set_icon(self.setting.icon)
        self.ship = Ship(Setting())
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        # Создание экземпляра для игровой статистики
        self.status = GameStatus(self)
        # Создание панели для хранения статистики и результатов
        self.sb = Scoreboard(self)
        # Создание кнопки Play
        self.play_button = Button(self, "Play")

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # Запускает новую игру при нажатии на кнопу Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.status.game_active:
            # Сброс игровых настроек
            self.setting.initialize_dinamic_setting()
            # Сброс игровой статистики
            self.status.reset_status()
            self.status.game_active = True
            self.sb.prep_score()
            self.sb.prep_ships()
            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.center_ship()

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
        elif event.key == pygame.K_p:
            self.status.game_active = True

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
        # Кнопка Play отображается в том случае если игра не активна
        if not self.status.game_active:
            self.play_button.draw_button()
        # Вывод информации о счёте
        self.sb.show_score()
        """Отображение последнего экрана"""
        pygame.display.flip()

    def _update_bullet(self):
        # Удаление старых снарядов и вывод на экран новых
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_bullet_alien_collision(self):
        # Удаление пришельцев и снарядов которые участвуют в коллизиях
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.setting.increase_speed()

            # Увеличение уровня
            self.status.level += 1
            self.sb.prep_level()
        if collisions:
            for alien in collisions.values():
                self.status.score += self.setting.alien_points * len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()

    def center_ship(self):
        # Размещение корабля в центре нижней стороны
        self.ship.rect.midbottom = self.ship.screen_rect.midbottom
        self.ship.x = float(self.ship.rect.x)

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцами"""
        if self.status.ship_left > 1:
            # Уменьшение ship_left
            self.status.ship_left -= 1
            self.sb.prep_ships()
            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и корабля
            self._create_fleet()
            self.center_ship()
            # Пауза
            sleep(1)
        else:
            self.status.game_active = False

    def _check_aliens_bottom(self):
        """Проверяет достигли ли пришельцы нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            self._ship_hit()
            break

    def _update_aliens(self):
        # Обновление позиции всех пришельцев на флоте
        self._check_fleet_edges()
        self.aliens.update()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            self._update_screen()
            if self.status.game_active:
                self._update_bullet()
                self._update_aliens()
