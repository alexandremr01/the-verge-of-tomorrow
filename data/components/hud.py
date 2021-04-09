import pygame
import numpy as np
from pygame.locals import K_1, K_2, K_3, K_w, K_a, K_s, K_d, K_LSHIFT
from ..constants import TIME_BETWEEN_COLLISIONS, BLACK
from ..constants import WEAPON_K1_DELAY, WEAPON_K2_DELAY, WEAPON_K3_DELAY, \
                        WEAPON_K1_INITIAL_BULLET, WEAPON_K2_INITIAL_BULLET, \
                        WEAPON_K3_INITIAL_BULLET, WEAPON_K1_MAX_BULLET, WEAPON_K2_MAX_BULLET, \
                        WEAPON_K3_MAX_BULLET, TIME_BETWEEN_HEARTBEAT

class Hud:
    """
    Heads-up display containing player's status and score.
    """

    def __init__(self, max_health, items_graphics, status_bar_graphics, status):
        self.score = 0

        self.heart = [1] * max_health
        self.heart_sprites = [items_graphics.get_image(5), items_graphics.get_image(9), items_graphics.get_image(4)]
        self.heart_positions = [(10 + 35 * i, 745) for i in range(max_health)]

        self.current_weapon = 0
        self.weapon_sprites = [pygame.transform.scale(items_graphics.get_image(7), (90, 90)),
                               pygame.transform.scale(items_graphics.get_image(6), (90, 90)),
                               pygame.transform.scale(items_graphics.get_image(8), (90, 90))]
        self.weapon_position = (385, 715)

        self.font = pygame.font.Font('./resources/fonts/ARCADECLASSIC.TTF', 30)
        self.small_font = pygame.font.Font('./resources/fonts/ARCADECLASSIC.TTF', 26)

        weapon_k1_ammo = str(WEAPON_K1_INITIAL_BULLET) + '  !' + str(WEAPON_K1_MAX_BULLET)
        weapon_k2_ammo = str(WEAPON_K2_INITIAL_BULLET) + '  !' + str(WEAPON_K2_MAX_BULLET)
        weapon_k3_ammo = str(WEAPON_K3_INITIAL_BULLET) + '  !' + str(WEAPON_K3_MAX_BULLET)
        self.ammo_surface = [self.small_font.render(weapon_k1_ammo, False, BLACK),
                             self.small_font.render(weapon_k2_ammo, False, BLACK),
                             self.small_font.render(weapon_k3_ammo, False, BLACK)]
        self.ammo_position = {6: (548, 740),
                              7: (542, 740),
                              8: (540, 740),
                              9: (530, 740)}
        self.ammo_current_position = [self.ammo_position[len(weapon_k1_ammo)],
                                      self.ammo_position[len(weapon_k2_ammo)],
                                      self.ammo_position[len(weapon_k3_ammo)]]

        self.score_num_surface = self.font.render('0', False, BLACK)
        self.score_num_rect = self.score_num_surface.get_rect(center=(685, 755))
        self.score_num = 0

        self.status_bar = status_bar_graphics.get_image(0)
        self.status_bar_position = (0, 700)
        self.status = self.font.render(status, False, BLACK)
        self.status_rect = self.status.get_rect(center=(280, 755))

    def set_ammo(self, weapon_type, value):
        """
        Changes ammo value of a given weapon
        """
        if weapon_type == K_1:
            weapon_k1_ammo = str(value) + '  !' + str(WEAPON_K1_MAX_BULLET)
            self.ammo_surface[0] = self.small_font.render(weapon_k1_ammo, False, BLACK)
            self.ammo_current_position[0] = self.ammo_position[len(weapon_k1_ammo)]
        elif weapon_type == K_2:
            weapon_k2_ammo = str(value) + '  !' + str(WEAPON_K2_MAX_BULLET)
            self.ammo_surface[1] = self.small_font.render(weapon_k2_ammo, False, BLACK)
            self.ammo_current_position[1] = self.ammo_position[len(weapon_k2_ammo)]
        elif weapon_type == K_3:
            weapon_k3_ammo = str(value) + '  !' + str(WEAPON_K3_MAX_BULLET)
            self.ammo_surface[2] = self.small_font.render(weapon_k3_ammo, False, BLACK)
            self.ammo_current_position[2] = self.ammo_position[len(weapon_k3_ammo)]

    def set_weapon(self, key):
        """
        Changes the current weapon
        """
        if key == K_1:
            self.current_weapon = 0
        elif key == K_2:
            self.current_weapon = 1
        elif key == K_3:
            self.current_weapon = 2

    def increase_score(self, delta_score):
        """
        Increases player's score
        """
        self.score_num += delta_score
        self.score_num_surface = self.font.render(str(self.score_num), False, BLACK)
        self.score = self.score_num

    def set_health(self, health):
        """
        Changes player's health
        """
        for i in range(len(self.heart)):
            if health == 0.5:
                self.heart[i] = 0.5
                health = 0
            elif health > 0:
                self.heart[i] = 1
                health -= 1
            else:
                self.heart[i] = 0

    def set_status(self, status):
        """
        Changes the player's status
        """
        self.status = self.font.render(status, False, BLACK)

    def draw(self, screen):
        """
        Draws the heads-up display
        """
        screen.blit_rel(self.status_bar, self.status_bar_position)
        for i in range(len(self.heart)):
            if self.heart[i] == 0:
                screen.blit_rel(self.heart_sprites[0], self.heart_positions[i])
            elif self.heart[i] == 0.5:
                screen.blit_rel(self.heart_sprites[1], self.heart_positions[i])
            else:
                screen.blit_rel(self.heart_sprites[2], self.heart_positions[i])
        screen.blit_rel(self.weapon_sprites[self.current_weapon], self.weapon_position)
        screen.blit_rel(self.ammo_surface[self.current_weapon],
                        self.ammo_current_position[self.current_weapon])
        screen.blit_rel(self.score_num_surface, self.score_num_rect)
        screen.blit_rel(self.status, self.status_rect)

    def get_score(self):
        """
        Returns player's total score
        """
        return self.score
