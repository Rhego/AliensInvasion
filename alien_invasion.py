import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Aliens
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:

    def __init__(self):
        """Inicializa el juego y crea los recursos necesarios para el juego"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, 'Play')

        #print(self.ship.rect.midbottom)

    def run_game(self):
        """Corre el loop principal para arrancar el juego"""

        while True:
            self._check_event()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            #print(self.ship.rect.y)
           #print(self.ship.rect.x)

    def _ship_hit(self):
        """Clase usada para controlar las acciones cuando una nave es golpeada"""

        if self.stats.ships_left > 0:
            #Decrementa el numero de naves
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Limpia los grupos de aliens y balas
            self.aliens.empty()
            self.bullets.empty()
            #Crea una nueva flota de aliens y centra la nave
            self._create_fleet()
            self.ship.center_ship()
            #Pausa
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            print("Game over")


    def _update_aliens(self):
        """Actualiza la posicion de los Aliens"""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Revisa si un alien llego a la parte de abajo de la pantalla
        self._check_alien_bottom()

    def _check_alien_bottom(self):
        """Chequea si los alien llegaron a la parte baja de la pantalla"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _create_fleet(self):
        """Create un grupo de aliens"""
        alien = Aliens(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        #Determina el numero de columnas que caben en la pantalla
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        #Crea el grupo de aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):
        #Crea un alien
        alien = Aliens(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Chequea si los aliens llegaron al borde la pantalla"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Cambia la direccion de la flota de aliens"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_bullets(self):
        self.bullets.update()
            #Elimina las balas cuando desaparecen de la pantalla
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        self._check_bullet_alien_collision()

   
    def _check_bullet_alien_collision(self):
           #Chequea si alguna bala colisiono con un alien
        collision = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collision:
            for aliens in collision.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                print(collision.values())
                print(len(aliens))
            self.sb.prep_score()
            self.sb.check_high_score()
        #Vuelve a creear una flota de aliens
        if not self.aliens:
            #Destruye las balas existentes y crea una nueva flota
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()



    def _check_event(self):
        """Responde a los eventos de puslados de teclas o movientos del mouse"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydow_events(event)
            elif event.type == pygame.KEYUP:
                self._check_up_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Inicia un nuevo juego cuando el jugador le da click al boton PLAY"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Reinicia las estadisticas del juego
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self._create_fleet()
            self.ship.center_ship()
            #Esconde el cursor
            pygame.mouse.set_visible(False)


    def _check_keydow_events(self, event):
        """Responde cuando una tecla es presionada"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_up_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _update_screen(self):
        """Actualiza la pantalla """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.sb.show_score()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _fire_bullet(self):
        """Crea una nueva bala y la agrega al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


if __name__ == "__main__":
    #"""Instancia el juego y crea la pantalla principal"""
    ai = AlienInvasion()
    ai.run_game()