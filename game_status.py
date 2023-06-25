class GameStatus:
    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.setting = ai_game.setting
        self.reset_status()
        self.score = 0
        # Игра запускается в не активном состояние
        self.game_active = False
        # Рекорд не должен сбрасываться
        self.high_score = 0

    def reset_status(self):
        """Инициализирует статистику изменяющеюся в ходе игры"""
        self.ship_left = self.setting.ship_limit
