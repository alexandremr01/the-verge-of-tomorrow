"""
Module containing player related abstractions.
The player being controlled by the user.
"""

import pygame
import numpy as np
from pygame.locals import K_1, K_2, K_3, K_w, K_a, K_s, K_d, K_LSHIFT

from ..utils import RandomEventGenerator, rotate
from . import player_state
from .hud import Hud
from .bag import Bag
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
from ..constants import PLAYER_INITIAL_HEALTH, PLAYER_INITIAL_VELOCITY
from ..constants import TIME_BETWEEN_COLLISIONS
from ..constants import TIME_BETWEEN_HEARTBEAT
from ..setup import graphics_dict
from .base.entity import Entity
from .projectiles import Projectiles
from .player_state import PlayerStateFSM
from ..setup import sound_dict
from data.components.weapon import Uzi, Shotgun, AK47


class Player(Entity):
    """
    Main character class
    """

    def __init__(self):
        super().__init__(np.array([0, 0]), graphics_dict['player'].get_image(0, (50, 50)))
        self.health = PLAYER_INITIAL_HEALTH
        self.direction = 0
        self.state = PlayerStateFSM()
        self.hud = Hud(self.health, graphics_dict['items'], graphics_dict['status_bar'], self.state.get_state_name())
        self.states = []
        self.projectiles = Projectiles()
        for i in range(graphics_dict['player'].get_size()):
            self.states.append(graphics_dict['player'].get_image(i, (50, 50)))
        self.weapon = self.states[0]
        self.current_weapon = self.states[0]
        self.last_collision_time = 0
        self.last_bleeding_time = 0
        self.last_shoot_time = [0, 0, 0]
        self.last_heartbeat_time = 0
        self.weapons = {"Uzi": Uzi(), "AK47": AK47(), "Shotgun": Shotgun()}
        self.current_weapon_name = "Uzi"
        self.small_font = pygame.font.Font('./resources/fonts/ARCADE_N.TTF', 20)

        self.text = None
        self.text_expiration_time = 0

        self.bag = Bag(graphics_dict['items'], graphics_dict['bag'])

        self.original_polygon_points = np.array(
            [(-220, -220), (SCREEN_WIDTH, -220), (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
             (SCREEN_WIDTH + 220, SCREEN_HEIGHT + 220), (-220, SCREEN_HEIGHT + 220)])
        self.polygon_points = self.original_polygon_points
        self.mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.polygon(self.mask, BLACK, self.polygon_points)
        self.last_angle = 0

        self.bullets = {}
        for weapon_name in self.weapons:
            self.bullets[weapon_name] = self.weapons[weapon_name].get_initial_ammo()

        debuf_probs = {
            player_state.SLOW_EVENT: 0.25,
            player_state.BLEED_EVENT: 0.2
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
            self.current_weapon_name = "Uzi"
            self.update_sprite(self.states[0])
        elif key == K_2:
            self.weapon = self.states[1]
            self.current_weapon_name = "AK47"
            self.update_sprite(self.states[1])
        elif key == K_3:
            self.weapon = self.states[2]
            self.current_weapon_name = "Shotgun"
            self.update_sprite(self.states[2])

        self.hud.set_weapon(self.weapons[self.current_weapon_name])
        self.current_weapon = self.weapon

    def update(self, key=None):
        """
        Updates the current player's state and heads-up display.
        """
        if key in [K_1, K_2, K_3]:
            self.set_weapon(key)
        elif key is K_LSHIFT:
            self.current_weapon = self.states[3]
            self.update_sprite(self.states[3])
        else:
            self.current_weapon = self.weapon
            self.update_sprite(self.current_weapon)

    def get_velocity(self):
        """
        Updates the current player's state and heads-up display.
        """
        return self.state.get_velocity()

    def update_state(self, time):
        if time > self.text_expiration_time:
            self.text = None

        if self.health <= 1 and time - self.last_heartbeat_time >= TIME_BETWEEN_HEARTBEAT:
            self.last_heartbeat_time = time
            sound_dict['heartbeat'].play()
        if self.state.get_state() == player_state.BleedingState and time - self.last_bleeding_time > player_state.BLEEDING_INTERVAL:
            self.hurt(player_state.BLEEDING_DAMAGE)
            self.last_bleeding_time = time
        self.state.update(time)
        self.hud.set_health(self.health)
        self.hud.set_status(self.state.get_state_name())

    def write(self, text, time, duration):
        self.text_expiration_time = time + duration
        self.text = text

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

        for i in range(len(self.original_polygon_points)):
            self.polygon_points[i] = rotate((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), self.original_polygon_points[i],
                                            (angle - self.last_angle))
        self.mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32).convert_alpha()

        pygame.draw.polygon(self.mask, BLACK, self.polygon_points)

        self.update_sprite(self.current_weapon, -angle)
        self.projectiles.update()
        self.last_angle = angle

    def shoot(self, time):
        """
        Shoots a projectile
        """
        can_shoot = False
        if time - self.last_shoot_time[0] >= self.weapons[self.current_weapon_name].get_delay():
            if self.bullets[self.current_weapon_name] - 1 >= 0:
                self.bullets[self.current_weapon_name] -= 1
                self.last_shoot_time[0] = time
                can_shoot = True
                self.update_ammo()
                sound_dict[self.current_weapon_name].play()

        if can_shoot:
            weapon_position = (30 * np.cos(np.radians(-self.direction + 20)),
                               25 * np.sin(np.radians(-self.direction + 20)))
            damage = self.state.get_damage(self.weapons[self.current_weapon_name].get_damage())
            self.projectiles.add_bullet(self.get_position() + weapon_position,
                                        weapon_position,
                                        -self.direction,
                                        self.weapons[self.current_weapon_name], damage)

    def update_ammo(self):
        """
        Update ammo for all weapons.
        """
        for weapon_name in self.weapons:
            self.hud.set_ammo(self.weapons[weapon_name], self.bullets[weapon_name])

    def draw(self, screen, is_day):
        """
        Draws the player's animation
        """
        if not is_day:
            screen.blit_rel(self.mask, (0, 0))
        super().draw(screen)

        if self.text is not None:
            if is_day:
                surface_text = self.small_font.render(self.text, False, BLACK)
                screen.blit_rel(surface_text, (SCREEN_WIDTH / 2 - 20 - len(self.text), SCREEN_HEIGHT / 2 - 50))
            else:
                surface_text = self.small_font.render(self.text, False, WHITE)
                screen.blit_rel(surface_text, (SCREEN_WIDTH / 2 - 20 - len(self.text), SCREEN_HEIGHT / 2 - 50))

        self.projectiles.draw(screen)

        self.hud.draw(screen)
        self.bag.draw(screen)

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
        debuff = self.debuf_generator.generate()
        self.state.send_event(debuff, time)
        if debuff == player_state.BLEED_EVENT:
            self.last_bleeding_time = time

    def handle_collision(self, enemy, time):
        """
        Handle collisions between player and enemy.
        """
        if time - self.last_collision_time < TIME_BETWEEN_COLLISIONS:
            return
        collide = pygame.sprite.collide_rect(self.get_sprite(), enemy.get_sprite())
        if collide:
            self.apply_random_debuff(time)
            self.hurt(enemy.get_damage())
            self.hud.set_health(self.health)
            self.hud.set_status(self.state.get_state_name())
            self.last_collision_time = time
            self.update_state(time)
