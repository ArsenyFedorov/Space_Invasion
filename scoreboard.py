import pygame.font


class Scoreboard():
    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчёта очков"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.setting = ai_game.setting
        self.status = ai_game.status
        # Настройки шрифта для вывода текста
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения
        self.prep_score()
        self.prep_high_score()

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

    def show_score(self):
        """Выводит счёт на экран"""
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.score_image, self.score_rect)

    def check_high_score(self):
        """Проверяет на наличие нового рекорда"""
        if self.status.score > self.status.high_score:
            self.status.high_score = self.status.score
            self.prep_score()