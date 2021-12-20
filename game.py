"""matthis meunier 1 phenix commence le 01/11/2021"""
import pygame
import pytmx
import pyscroll

from dialogs import Dialogs
from map import MapManager

from player import Player


class Game:

    def __init__(self):
        # creation de la fenetre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jeux principale")

        # generer le joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = Dialogs()


        # toucche de déplacement

    def touche(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()


    def update(self):
        self.map_manager.update()

    def run(self):

        # FPS du jeu

        clock = pygame.time.Clock()

        # boucle du jeux
        running = True

        while running:

            self.player.save_location()
            self.touche()
            self.update()  # creer les calque
            self.map_manager.draw()
            self.dialog_box.affichage(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)

            clock.tick(64)

    pygame.quit()