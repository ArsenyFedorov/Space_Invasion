import pygame.font


class Button():
    def __init__(self, ai_game, msg):
        """Инициализирует атрибут кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Назначение размера и свойств кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        # Создание кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # Сообщение кнопки создаётся один раз
        self._prep_msg("Play")

    def _prep_msg(self, msg):
        # Преобразует msg в прямоугольник и выравнивает текс по центру
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Изображение пустой кнопки и вывод её на экран
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
