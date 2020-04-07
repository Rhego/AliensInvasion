import pygame
from pygame.sprite import Sprite

class Aliens(Sprite):
    """Clase que represeta un alien """
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Carga la imagen del alien
        self.image = pygame.image.load('images/Aranza_60x58.png')
        self.rect = self.image.get_rect()

        #Inicializa cada alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def update(self):
        """Moviente de los aliens a la Derecha o Izquierda"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        #self.x += self.settings.alien_speed
        self.rect.x = self.x

    def check_edges(self):
        """Retorna Verdadero si la flota de aliens se encuntra en el borde"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or  self.rect.left <= 0:
            return True
