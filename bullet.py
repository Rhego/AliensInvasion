import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Clase encargada de Dibujar las balas de la nave"""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #Crea la bala en la posicion correspondiente

        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
         self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #Almacena la posicion de la bala como decimal
        self.y = float(self.rect.y)

    def update(self):
        """Encargado de mover la posicion de la bala"""
        self.y -= self.settings.bullet_speed
        #Actualizal la posicion
        self.rect.y = self.y

    def draw_bullet(self):
        """Dibuja la bala en la pantalla"""
        pygame.draw.rect(self.screen, self.color, self.rect)





