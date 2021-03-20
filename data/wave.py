"""
Class responsible for keeping track of
the enemies of the game, as well as creating
them.
"""

from math import sin, cos
import numpy as np

from .utils import distance
from .constants import ENEMIES_INCREMENT_PER_WAVE, TIME_TO_SPAWN
from .constants import SPAWN_DISTANCE, DESPAWN_DISTANCE
from .components.enemies.zombie import Zombie

class Wave:
    """
    Keeps track of enemies, responsible
    for creation as well
    """
    def __init__(self, time):
        self.current_wave = 0

        self.current_wave_num_enemies = 0
        self.num_enemies_killed = 0
        self.num_enemies_to_spawn = 0
        self.total_enemies_killed = 0
        self.spawn_timer = time

        self.enemies = []
        self.wave_over = True

        self.new_wave()

    def new_wave(self):  # TODO: night/day dynamics
        """
        Creates a new wave, resetting its params.
        The number of players increases by 5 as each
        wave passes
        """
        self.wave_over = False
        self.current_wave += 1

        self.num_enemies_killed = 0
        self.current_wave_num_enemies = self.current_wave*ENEMIES_INCREMENT_PER_WAVE
        self.num_enemies_to_spawn = self.current_wave_num_enemies

    def generate_enemy(self, player_position):
        """
        Creates an enemy located on pos
        """
        theta = np.random.rand()
        spawn_vector = np.array([cos(theta), sin(theta)]) * SPAWN_DISTANCE
        new_enemy_pos = player_position + spawn_vector

        self.enemies.append(Zombie(new_enemy_pos))  # TODO: use more enemies
        self.num_enemies_to_spawn -= 1

    def update_alive_enemies(self, player_position):
        """
        Checks each enemy's health and distance to
        player to see if it continues alive or not
        """
        live_enemies = []
        for enemy in self.enemies:
            if enemy.health == 0:
                self.num_enemies_killed += 1
                self.total_enemies_killed += 1
            elif distance(enemy.get_position(), player_position) > DESPAWN_DISTANCE:
                self.num_enemies_to_spawn += 1
            else:
                live_enemies.append(enemy)
        self.enemies = live_enemies

    def update_enemies(self, player, time):
        """
        Updates enemies' states, spawning or despawning
        them if it is the case
        """
        for enemy in self.enemies:
            if not enemy.sprite.rect.colliderect(player.sprite.rect):
                enemy.ai_move(player.get_position())

        self.update_alive_enemies(player.get_position())
        if time - self.spawn_timer > TIME_TO_SPAWN and self.num_enemies_to_spawn > 0:
            self.generate_enemy(player.get_position())
            self.spawn_timer = time

        if self.num_enemies_killed == self.current_wave_num_enemies:
            self.wave_over = True

    def finished(self):
        """
        Query to whether current wave is over or not
        """
        return self.wave_over
