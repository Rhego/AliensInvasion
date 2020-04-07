import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Clase para controlar la Nave"""

    def __init__(self, ai_game):
        """Inicializa la Nave y la coloca en su posicion inicial"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Carga la imagen de la nave
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Inicia la nave en la parte baja central de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom

        #Almacena en formato decimal el valor X
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

        #Moviente en Y
        self.y = float(self.rect.y)
        self.moving_up = False
        self.moving_down = False



    def update(self):
        """Actualiza el movimiento"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Dibju la nave en su posicion"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centra la nave en la pantalla"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
