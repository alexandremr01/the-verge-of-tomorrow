"""
Class responsible for keeping track of
the enemies of the game, as well as creating
them.
"""

from .constants import ENEMIES_INCREMENT_PER_WAVE

class Wave:
    """
    Keeps track of enemies, responsible
    for creation as well
    """
    def __init__(self):
        self.current_wave = 0

        self.current_wave_num_enemies = 0
        self.num_enemies_killed = 0
        self.num_enemies_to_spawn = 0
        self.total_enemies_killed = 0

        self.wave_over = True

    def new_wave(self):
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

    def notify_kill(self):
        """
        This function is called when an enemy is
        killed
        """
        if self.wave_over:
            print('Error: wave is finished and kill was notified')
            return

        self.num_enemies_killed += 1
        self.total_enemies_killed += 1

        if self.num_enemies_killed == self.current_wave_num_enemies:
            self.wave_over = True

    def notify_despawn(self):
        """
        This function is called when an enemy is
        despawned and has to be recreated
        """
        if self.num_enemies_to_spawn + 1 > self.current_wave_num_enemies:
            print('Error: there are more enemies to spawn than it should be')
            return
        if self.wave_over:
            print('Error: wave is finished and there was despawn')

        self.num_enemies_to_spawn += 1

    def generate_enemy(self):
        pass

    def spawns_left(self):
        """
        Query to whether there still are enemies
        left to spawn
        """
        return self.num_enemies_to_spawn > 0

    def finished(self):
        """
        Query to whether current wave is over or not
        """
        return self.wave_over
