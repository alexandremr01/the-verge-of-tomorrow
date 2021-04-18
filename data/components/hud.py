import pygame
from ..constants import BLACK
from data.components.weapon import Uzi, Shotgun, AK47


class Hud:
    """
    Heads-up display containing player's status and score.
    """

    def __init__(self, max_health, items_graphics, status_bar_graphics, status):
        self.score = 0

        self.heart = [1] * max_health
        self.heart_sprites = [items_graphics.get_image(5), items_graphics.get_image(9), items_graphics.get_image(4)]
        self.heart_positions = [(10 + 35 * i, 745) for i in range(max_health)]


        self.current_weapon_name = "Uzi"
        self.weapon_position = (385, 715)

        self.font = pygame.font.Font('./resources/fonts/ARCADECLASSIC.TTF', 30)
        self.small_font = pygame.font.Font('./resources/fonts/ARCADECLASSIC.TTF', 26)

        self.ammo_position = {6: (548, 740),
                              7: (542, 740),
                              8: (540, 740),
                              9: (530, 740)}

        weapon_types = [Uzi(), AK47(), Shotgun()]
        self.ammo_surface = {}
        self.ammo_current_position = {}
        self.weapon_sprites = {}
        for weapon in weapon_types:
            weapon_ammo = str(weapon.get_initial_ammo()) + '  !' + str(weapon.get_max_ammo())
            self.ammo_surface[weapon.get_name()] = self.small_font.render(weapon_ammo, False, BLACK)
            self.ammo_current_position[weapon.get_name()] = self.ammo_position[len(weapon_ammo)]
            self.weapon_sprites[weapon.get_name()] = pygame.transform.scale(items_graphics.get_image(
                                                                 weapon.get_image_index()), (90, 90))

        self.score_num_surface = self.font.render('0', False, BLACK)
        self.score_num_rect = self.score_num_surface.get_rect(center=(685, 755))
        self.score_num = 0

        self.status_bar = status_bar_graphics.get_image(0)
        self.status_bar_position = (0, 700)
        self.status = self.font.render(status, False, BLACK)
        self.status_rect = self.status.get_rect(center=(280, 755))

    def set_ammo(self, weapon, value):
        """
        Changes ammo value of a given weapon
        """
        weapon_ammo = str(value) + '  !' + str(weapon.get_max_ammo())
        self.ammo_surface[weapon.get_name()] = self.small_font.render(weapon_ammo, False, BLACK)
        self.ammo_current_position[weapon.get_name()] = self.ammo_position[len(weapon_ammo)]

    def set_weapon(self, weapon):
        """
        Changes the current weapon
        """
        self.current_weapon_name = weapon.get_name()

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
        screen.blit_rel(self.weapon_sprites[self.current_weapon_name], self.weapon_position)
        screen.blit_rel(self.ammo_surface[self.current_weapon_name],
                        self.ammo_current_position[self.current_weapon_name])
        screen.blit_rel(self.score_num_surface, self.score_num_rect)
        screen.blit_rel(self.status, self.status_rect)

    def get_score(self):
        """
        Returns player's total score
        """
        return self.score
