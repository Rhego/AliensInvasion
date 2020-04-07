class GameStats:
    """Se encarga de manejar las estadisticas"""

    def __init__(self, ai_game):
        """Inicializa todas las estadisticas"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Variable que controla cuando inicia o termina el juego
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """reinicia todo las estadisticas"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

