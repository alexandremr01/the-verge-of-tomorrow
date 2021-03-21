"""
Module containing player related abstractions.
The player being controlled by the user.
"""

import pygame
import numpy as np
from pygame.locals import K_1, K_2, K_3, K_w, K_a, K_s, K_d

from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, \
    PLAYER_INITIAL_HEALTH, PLAYER_INITIAL_VELOCITY, TIME_BETWEEN_COLLISIONS, BLACK
from ..setup import graphics_dict
from .base.entity import Entity
from .projectiles import Projectiles


class Hud:
    """
    Heads-up display containing player's status and score.
    """
    def __init__(self, max_health, items_graphics):
        self.heart = [True] * max_health
        self.heart_sprites = [items_graphics.get_image(4), items_graphics.get_image(5)]
        self.heart_positions = [(20+35*i, 20) for i in range(max_health)]
        self.current_weapon = 0
        self.weapon_sprites = [pygame.transform.scale(items_graphics.get_image(7), (90, 90)),
                               pygame.transform.scale(items_graphics.get_image(6), (90, 90)), 
                               pygame.transform.scale(items_graphics.get_image(8), (90, 90))]
        self.weapon_position = (670, 650)
        self.font = pygame.font.SysFont('Arial', 30)
        self.score_surface = self.font.render('SCORE', False, BLACK)
        self.score_rect = self.score_surface.get_rect(center=(100, 750))
        self.weapon_surface = self.font.render('WEAPON', False, BLACK)
        self.weapon_rect = self.score_surface.get_rect(center=(700, 750))
        self.score_num_surface = self.font.render('0', False, BLACK)
        self.score_num_rect = self.score_surface.get_rect(center=(100, 710))
        self.score_num = 0

    def update(self, key, health=None, delta_score=None):  # TODO: include status
        """
        Updates all the hud's elements
        """
        if delta_score is not None:
            self.score_num += delta_score
            self.score_num_surface = self.font.render(str(self.score_num), False, BLACK)
        if key == K_1:
            self.current_weapon = 0
        elif key == K_2:
            self.current_weapon = 1
        elif key == K_3:
            self.current_weapon = 2
        if health is not None:
            self.heart[health:] = [False] * len(self.heart[health:])

    def draw(self, screen):
        """
        Draws the heads-up display
        """
        for i in range(len(self.heart)):
            if self.heart[i] is True:
                screen.blit_rel(self.heart_sprites[0], self.heart_positions[i])
            else:
                screen.blit_rel(self.heart_sprites[1], self.heart_positions[i])
        screen.blit_rel(self.weapon_sprites[self.current_weapon], self.weapon_position)
        screen.blit_rel(self.score_surface, self.score_rect)
        screen.blit_rel(self.weapon_surface, self.weapon_rect)
        screen.blit_rel(self.score_num_surface, self.score_num_rect)


class Player(Entity):
    """
    Main character class
    """
    def __init__(self):
        super().__init__(np.array([0, 0]), graphics_dict['player'].get_image(0, (50, 50)))
        self.health = PLAYER_INITIAL_HEALTH
        self.velocity = PLAYER_INITIAL_VELOCITY
        self.score = 0
        self.direction = 0
        self.hud = Hud(self.health, graphics_dict['items'])
        self.states = []
        self.projectiles = Projectiles()
        for i in range(graphics_dict['player'].get_size()):
            self.states.append(graphics_dict['player'].get_image(i, (50, 50)))
        self.weapon = self.states[0]
        self.weapon_type = K_1
        self.current_state = self.states[0]
        self.last_collision_time = 0

    def get_hud(self):
        """
        Returns game's hud.
        """
        return self.hud

    def get_projectiles(self):
        """
        Returns player projectiles.
        """
        return self.projectiles

    def set_weapon(self, key):
        """
        Sets a weapon for the player
        """
        if key == K_1:
            self.weapon = self.states[0]
            self.weapon_type = K_1
            self.update_sprite(self.states[0])
            self.current_state = self.weapon
        elif key == K_2:
            self.weapon = self.states[1]
            self.weapon_type = K_2
            self.update_sprite(self.states[1])
            self.current_state = self.weapon
        elif key == K_3:
            self.weapon = self.states[2]
            self.weapon_type = K_3
            self.update_sprite(self.states[2])
            self.current_state = self.weapon

    def update(self, key=None):
        """
        Updates the current player's state and heads-up display.
        """
        if key in [K_1, K_2, K_3]:
            self.set_weapon(key)
        elif key in [K_w, K_a, K_s, K_d]:
            self.current_state = self.states[3]
            self.update_sprite(self.states[3])
        else:
            self.current_state = self.weapon
            self.update_sprite(self.current_state)
        self.hud.update(key)

    def update_direction(self):
        """
        Updates the current player's direction.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_coordinate = mouse_x - (SCREEN_WIDTH // 2)
        y_coordinate = mouse_y - (SCREEN_HEIGHT // 2)
        angle = int(np.degrees(np.arctan2(y_coordinate, x_coordinate)))
        self.direction = -angle
        self.update_sprite(self.current_state, -angle)
        self.projectiles.update()

    def shoot(self):
        """
        Shoots a projectile
        """
        weapon_position = (30 * np.cos(np.radians(-self.direction+20)), 
                           25 * np.sin(np.radians(-self.direction+20)))
        self.projectiles.add_bullet(self.get_position() + weapon_position,
                                    weapon_position,
                                    -self.direction, 
                                    self.weapon_type)

    def draw(self, screen):
        """
        Draws the player's animation
        """
        super().draw(screen)
        self.projectiles.draw(screen)
        self.hud.draw(screen)

    def hurt(self, damage):
        """
        Decreases the player's health by damage.
        """
        self.health -= damage

    def is_alive(self):
        """
        Returns a boolean indicating whether player is alive or not
        """
        return self.health > 0

    def handle_collision(self, zombie, time):
        """
        Handle collisions between player and zombie.
        """
        if time - self.last_collision_time < TIME_BETWEEN_COLLISIONS:
            return
        collide = pygame.sprite.collide_rect(self.get_sprite(), zombie.get_sprite())
        if collide:
            self.hurt(zombie.get_damage())
            self.hud.update(None, self.health)
            self.last_collision_time = time