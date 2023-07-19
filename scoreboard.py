import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчёта очков"""
        self.screen = ai_game.screen
        self.ai_game = ai_game
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.setting
        self.status = ai_game.status
        # Настройки шрифта для вывода текста
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_high_score(self):
        """Преобразует рекордный счёт на экран"""
        high_score = round(self.status.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.setting.bg_color)
        # Выравнивание рекорда
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop
        self.screen_rect.top = self.score_rect.top

    def prep_score(self):
        """Преабразует текущий счёт в изображение"""
        round_score = round(self.status.score, -1)
        score_str = "{:,}".format(round_score)
        score_str = str(self.status.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.setting.bg_color)
        # Вывод счёта в правой части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        """Преобразует уровень в графическое изображение"""
        level_str = str(self.status.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.setting.bg_color)
        # Уровень выводится под текущим счётом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Сообщает количество оставшихся кораблей"""
        self.ships = Group()
        for ship_numbers in range(self.status.ship_left):
            ship = Ship(self.ai_game.setting)
            ship.rect.x = 10 + ship_numbers * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Выводит счёт на экран, рекорд и номер уровня и количество жизней"""
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #for ship in self.ships:
            #self.ships.draw(self.screen, ship)

    def check_high_score(self):
        """Проверяет на наличие нового рекорда"""
        if self.status.score > self.status.high_score:
            self.status.high_score = self.status.score
            self.prep_score()
