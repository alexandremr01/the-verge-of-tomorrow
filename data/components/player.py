"""
Module containing player related abstractions.
The player being controlled by the user.
"""

import pygame
import numpy as np
from pygame.locals import K_1, K_2, K_3, K_w, K_a, K_s, K_d, K_LSHIFT
import random

from ..utils import RandomEventGenerator
from . import player_state
from .hud import Hud
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..constants import PLAYER_INITIAL_HEALTH, PLAYER_INITIAL_VELOCITY 
from ..constants import TIME_BETWEEN_COLLISIONS, BLACK
from ..constants import WEAPON_K1_DELAY, WEAPON_K2_DELAY, WEAPON_K3_DELAY, \
                        WEAPON_K1_INITIAL_BULLET, WEAPON_K2_INITIAL_BULLET, \
                        WEAPON_K3_INITIAL_BULLET, WEAPON_K1_MAX_BULLET, WEAPON_K2_MAX_BULLET, \
                        WEAPON_K3_MAX_BULLET, TIME_BETWEEN_HEARTBEAT
from ..setup import graphics_dict
from .base.entity import Entity
from .projectiles import Projectiles
from .player_state import PlayerStateFSM
from ..setup import sound_dict

class Player(Entity):
    """
    Main character class
    """
    def __init__(self):
        super().__init__(np.array([0, 0]), graphics_dict['player'].get_image(0, (50, 50)))
        self.health = PLAYER_INITIAL_HEALTH
        self.velocity = PLAYER_INITIAL_VELOCITY
        self.direction = 0
        self.state = PlayerStateFSM()
        self.hud = Hud(self.health, graphics_dict['items'], graphics_dict['status_bar'], self.state.get_state_name())
        self.states = []
        self.projectiles = Projectiles()
        for i in range(graphics_dict['player'].get_size()):
            self.states.append(graphics_dict['player'].get_image(i, (50, 50)))
        self.weapon = self.states[0]
        self.weapon_type = K_1
        self.current_weapon = self.states[0]
        self.last_collision_time = 0
        self.last_bleeding_time = 0
        self.last_shoot_time = [0, 0, 0]
        self.last_heartbeat_time = 0
        self.bullets = {K_1 : WEAPON_K1_INITIAL_BULLET, 
                        K_2 : WEAPON_K2_INITIAL_BULLET, 
                        K_3 : WEAPON_K3_INITIAL_BULLET}

        debuf_probs = {
            player_state.SLOW_EVENT: 0.1,
            player_state.BLEED_EVENT: 0.1
        }
        self.debuf_generator = RandomEventGenerator(debuf_probs, null_event=None)


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

    def get_score(self):
        """
        Returns the total player's score
        """
        return self.hud.get_score()

    def set_weapon(self, key):
        """
        Sets a weapon for the player
        """
        if key == K_1:
            self.weapon = self.states[0]
            self.weapon_type = K_1
            self.update_sprite(self.states[0])
            self.hud.set_weapon(K_1)
            self.current_weapon = self.weapon
        elif key == K_2:
            self.weapon = self.states[1]
            self.weapon_type = K_2
            self.update_sprite(self.states[1])
            self.hud.set_weapon(K_2)
            self.current_weapon = self.weapon
        elif key == K_3:
            self.weapon = self.states[2]
            self.weapon_type = K_3
            self.update_sprite(self.states[2])
            self.hud.set_weapon(K_3)
            self.current_weapon = self.weapon

    def update(self, key=None):
        """
        Updates the current player's state and heads-up display.
        """
        if key in [K_1, K_2, K_3]:
            self.set_weapon(key)
        elif key in [K_w, K_a, K_s, K_d]:
            self.current_weapon = self.states[3]
            self.update_sprite(self.states[3])
        else:
            self.current_weapon = self.weapon
            self.update_sprite(self.current_weapon)

    def get_velocity(self):
        """
        Updates the current player's state and heads-up display.
        """
        state = self.state.get_state()
        if state == player_state.RunningState:
            return 2*self.velocity
        elif state == player_state.SlowState:
            return 0.8*self.velocity
        return self.velocity

    def update_state(self, time):
        if self.health <= 1 and time - self.last_heartbeat_time >= TIME_BETWEEN_HEARTBEAT:
            self.last_heartbeat_time = time
            sound_dict['heartbeat'].play()
        if self.state.get_state() == player_state.BleedingState and time - self.last_bleeding_time > player_state.BLEEDING_INTERVAL :
            self.hurt(player_state.BLEEDING_DAMAGE)
            self.last_bleeding_time = time
        self.state.update(time)
        self.hud.set_health(self.health)
        self.hud.set_status(self.state.get_state_name())

    def set_running(self, time):
        """
        Updates the current player's state and heads-up display.
        """
        self.state.send_event(player_state.RUN_EVENT, time)

    def stop_running(self, time):
        """
        Updates the current player's state and heads-up display.
        """
        self.state.send_event(player_state.STOP_RUN_EVENT, time)

    def update_direction(self):
        """
        Updates the current player's direction.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_coordinate = mouse_x - (SCREEN_WIDTH // 2)
        y_coordinate = mouse_y - (SCREEN_HEIGHT // 2)
        angle = int(np.degrees(np.arctan2(y_coordinate, x_coordinate)))
        self.direction = -angle
        self.update_sprite(self.current_weapon, -angle)
        self.projectiles.update()

    def shoot(self, time):
        """
        Shoots a projectile
        """
        can_shoot = False
        if self.weapon_type == K_1:
            if time - self.last_shoot_time[0] >= WEAPON_K1_DELAY:
                if self.bullets[K_1] - 1 >= 0:
                    self.bullets[K_1] -= 1
                    self.last_shoot_time[0] = time
                    can_shoot = True
                    self.hud.set_ammo(K_1, self.bullets[K_1])
                    sound_dict['WEAPON_K_1'].play()
        elif self.weapon_type == K_2:
            if time - self.last_shoot_time[1] >= WEAPON_K2_DELAY:
                if self.bullets[K_2] - 1 >= 0:
                    self.bullets[K_2] -= 1 
                    self.last_shoot_time[1] = time
                    can_shoot = True
                    self.hud.set_ammo(K_2, self.bullets[K_2])
                    sound_dict['WEAPON_K_2'].play()
        elif self.weapon_type == K_3:        
            if time - self.last_shoot_time[2] >= WEAPON_K3_DELAY:
                if self.bullets[K_3] - 1 >= 0:
                    self.bullets[K_3] -= 1
                    self.last_shoot_time[2] = time
                    can_shoot = True
                    self.hud.set_ammo(K_3, self.bullets[K_3])
                    sound_dict['WEAPON_K_3'].play()
        if can_shoot:
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
        sound_dict['hit_1'].play()

    def is_alive(self):
        """
        Returns a boolean indicating whether player is alive or not
        """
        return self.health > 0

    def apply_random_debuff(self, time):
        debuf = self.debuf_generator.generate()
        self.state.send_event(debuf, time)
        if debuf == player_state.BLEED_EVENT:
            self.last_bleeding_time = time

    def handle_collision(self, zombie, time):
        """
        Handle collisions between player and zombie.
        """
        if time - self.last_collision_time < TIME_BETWEEN_COLLISIONS:
            return
        collide = pygame.sprite.collide_rect(self.get_sprite(), zombie.get_sprite())
        if collide:
            self.apply_random_debuff(time)
            self.hurt(zombie.get_damage())
            self.hud.set_health(self.health)
            self.hud.set_status(self.state.get_state_name())
            self.last_collision_time = time
            self.update_state(time)

