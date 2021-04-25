"""
Class responsible for keeping track of
the enemies of the game, as well as creating
them.
"""

from math import sin, cos
import numpy as np
import pygame

from .utils import distance
from .constants import ENEMIES_INCREMENT_PER_WAVE, TIME_TO_SPAWN, BASE_FONT_DIR
from .constants import SPAWN_DISTANCE, DESPAWN_DISTANCE, FRAMES_TO_ENEMIES_TURN
from .constants import SHOW_WAVE_TIME, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from .components.enemies.zombie import Zombie
from .components.enemies.bat import Bat
from .components.enemies.giant import Giant

class Wave:
    """
    Keeps track of enemies, responsible
    for creation as well
    """

    def __init__(self, time):
        self.current_wave = 0
        self.enemiesTurn = 0

        self.current_wave_num_enemies = 0
        self.num_enemies_killed = 0
        self.num_enemies_to_spawn = 0
        self.total_enemies_killed = 0
        self.spawn_timer = time

        self.zombie_prob = 0.6
        self.bat_prob = 0.4
        self.giant_prob = 0.

        self.enemies = []
        self.despawned_enemies = []
        self.wave_over = True
        self.day = True

        self.show_wave = False
        self.show_wave_timer = 0
        self.wave_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 50)
        self.wave_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        self.daynight_font = pygame.font.Font(BASE_FONT_DIR + 'ARCADECLASSIC.TTF', 20)
        self.daynight_center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/3 + 50)

    def new_wave(self, time):
        """
        Creates a new wave, resetting its params.
        The number of players increases by 5 as each
        wave passes
        """
        self.wave_over = False
        self.show_wave = True
        self.show_wave_timer = time
        self.current_wave += 1

        if self.current_wave > 3: # after round 4, giants appear
            self.zombie_prob = 0.5
            self.bat_prob = 0.4
            self.giant_prob = 0.1

        if np.random.uniform(0, 1, 1)[0] > 0.5 and self.current_wave != 1:
            self.day = False
        else:
            self.day = True

        self.num_enemies_killed = 0
        self.current_wave_num_enemies = self.current_wave * ENEMIES_INCREMENT_PER_WAVE
        self.num_enemies_to_spawn = self.current_wave_num_enemies

    def generate_enemy(self, player_position):
        """
        Creates an enemy located on pos
        """
        theta = np.random.rand()
        spawn_vector = np.array([cos(theta), sin(theta)]) * SPAWN_DISTANCE
        new_enemy_pos = player_position + spawn_vector

        if len(self.despawned_enemies) > 0:
            respawned = self.despawned_enemies.pop()
            move_vector = new_enemy_pos - respawned.get_position()
            respawned.move(move_vector[0], move_vector[1])
            self.enemies.append(respawned)
        else:
            coin_flip = np.random.uniform(0, 1, 1)
            if coin_flip < self.zombie_prob:
                self.enemies.append(Zombie(new_enemy_pos))
            elif coin_flip < self.zombie_prob + self.bat_prob:
                self.enemies.append(Bat(new_enemy_pos))
            else:
                self.enemies.append(Giant(new_enemy_pos))

        self.num_enemies_to_spawn -= 1

    def update_alive_enemies(self, player_position, hud):
        """
        Checks each enemy's health and distance to
        player to see if it continues alive or not
        """
        live_enemies = []
        for enemy in self.enemies:
            if enemy.health == 0:
                self.num_enemies_killed += 1
                self.total_enemies_killed += 1
                hud.increase_score(enemy.score)
            elif distance(enemy.get_position(), player_position) > DESPAWN_DISTANCE:
                self.num_enemies_to_spawn += 1
                self.despawned_enemies.append(enemy)
            else:
                live_enemies.append(enemy)
        self.enemies = live_enemies

    def update_enemies(self, player, time, validate_pos):
        """
        Updates enemies' states, spawning or despawning
        them if it is the case
        """
        self.enemiesTurn += 1
        if self.enemiesTurn == FRAMES_TO_ENEMIES_TURN:
            for enemy in self.enemies:
                if not enemy.sprite.rect.colliderect(player.sprite.rect):
                    enemy.ai_move(player.get_position(), validate_pos)
            self.enemiesTurn = 0

        self.update_alive_enemies(player.get_position(), player.get_hud())
        if time - self.spawn_timer > TIME_TO_SPAWN and self.num_enemies_to_spawn > 0:
            self.generate_enemy(player.get_position())
            self.spawn_timer = time

        if self.num_enemies_killed == self.current_wave_num_enemies:
            self.wave_over = True

        for enemies in self.enemies:
            enemies.play_noise(time, player.get_position())

    def get_enemies(self):
        """
        Returns all the enemies alive.
        """
        return self.enemies

    def is_day(self):
        """
        Returns whether it's day or night
        """
        return self.day

    def finished(self):
        """
        Query to whether current wave is over or not
        """
        return self.wave_over

    def draw(self, screen, time):
        """
        Draws on player's screen number of enemies left and notifies
        player whether there is a new wave or not
        """
        time_passed = time - self.show_wave_timer
        if time - self.show_wave_timer < SHOW_WAVE_TIME:
            wave_surface = self.wave_font.render(('Wave ' + str(self.current_wave)), False, WHITE)
            wave_surface.set_alpha(255*(SHOW_WAVE_TIME - time_passed)/SHOW_WAVE_TIME)
            wave_rect = wave_surface.get_rect(center=self.wave_center)

            daynight_surface = None
            if self.day:
                daynight_surface = self.daynight_font.render(('day'), False, WHITE)
            else:
                daynight_surface = self.daynight_font.render(('night'), False, WHITE)
            daynight_rect = daynight_surface.get_rect(center=self.daynight_center)
            daynight_surface.set_alpha(255*(SHOW_WAVE_TIME - time_passed)/SHOW_WAVE_TIME)

            screen.blit_rel(daynight_surface, daynight_rect)
            screen.blit_rel(wave_surface, wave_rect)
