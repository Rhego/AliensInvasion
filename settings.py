class Settings:
    """Clase encargada de guardar todas las configuraciones"""

    def __init__(self):
        #Inicializa las configuraciones del juego

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #Bullets Settings
        self.bullet_width = 3000
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
        self.ship_limit = 3

    def initialize_dynamic_settings(self):
     #Aliens Settings

        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_points = 50


    def increase_speed(self):
        """Incrementa la velocidad"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)