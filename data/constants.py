"""
This module contains constant variables used throughout all
code
"""
import pygame
import numpy as np

# Screen
FRAMES_PER_SECOND = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_ARRAY = np.array([SCREEN_WIDTH, SCREEN_HEIGHT])
TRANSITION_BETWEEN_SCREENS = 5

# Colors (RGB format)
ORANGE = (250, 157, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Title Screen
TITLE_FRAMERATE = 150
TITLE_MESSAGE_FRAMERATE = 500

# Map
RENDER_STEPS = 24  # 16 IS ENOUGH TO NOT LAG
CHUNK_SIZE = 2400
CHUNK_ARRAY = np.array([CHUNK_SIZE, CHUNK_SIZE])
CHUNK_RECT = pygame.Rect((-CHUNK_SIZE/2, -CHUNK_SIZE/2), (CHUNK_SIZE, CHUNK_SIZE))
TOP_RECT = pygame.Rect((-CHUNK_SIZE/2, -CHUNK_SIZE/2), (CHUNK_SIZE, CHUNK_SIZE/3))
BOTTOM_RECT = pygame.Rect((-CHUNK_SIZE/2, -CHUNK_SIZE/2 + CHUNK_SIZE*2/3), (CHUNK_SIZE, CHUNK_SIZE/3))
LEFT_RECT = pygame.Rect((-CHUNK_SIZE/2, -CHUNK_SIZE/2), (CHUNK_SIZE/3, CHUNK_SIZE))
RIGHT_RECT = pygame.Rect((-CHUNK_SIZE/2 + CHUNK_SIZE*2/3, -CHUNK_SIZE/2), (CHUNK_SIZE/3, CHUNK_SIZE))
TILE_SIZE = 50
TILE_ARRAY = np.array([TILE_SIZE, TILE_SIZE])
CHUNK_TILE_RATIO = CHUNK_SIZE // TILE_SIZE
CHUNK_TILE_RATIO_STEPS = CHUNK_SIZE // TILE_SIZE // RENDER_STEPS

# Waves
ENEMIES_INCREMENT_PER_WAVE = 2
TIME_TO_SPAWN = 5*1000  # milliseconds
DAY_WAVE_DURATION = 3
NIGHT_WAVE_DURATION = 1

# Enemies
SPAWN_DISTANCE = 600
DESPAWN_DISTANCE = 800
DEFAULT_ENEMY_VELOCITY = 2
DEFAULT_ENEMY_HEALTH = 100
DEFAULT_ENEMY_DAMAGE = 1
ZOMBIE_VELOCITY = 2
ZOMBIE_HEALTH = 110
ZOMBIE_DAMAGE = 1
ZOMBIE_SCORE = 5
FRAMES_TO_ENEMIES_TURN = 2

# Player
PLAYER_INITIAL_HEALTH = 5
PLAYER_INITIAL_VELOCITY = 3
TIME_BETWEEN_COLLISIONS = 2*1000  # milliseconds
TIME_BETWEEN_HEARTBEAT = 2*1000 #milliseconds

# Bullet
BULLET_VELOCITY = 10
WEAPON_K1_DAMAGE = 20
WEAPON_K2_DAMAGE = 30
WEAPON_K3_DAMAGE = 40
WEAPON_K1_DELAY = 150 #milliseconds
WEAPON_K2_DELAY = 300 #milliseconds
WEAPON_K3_DELAY = 550 #milliseconds
WEAPON_K1_INITIAL_BULLET = 150
WEAPON_K2_INITIAL_BULLET = 30
WEAPON_K3_INITIAL_BULLET = 10
WEAPON_K1_MAX_BULLET = 150
WEAPON_K2_MAX_BULLET = 40
WEAPON_K3_MAX_BULLET = 20

# Directories
BASE_GRAPHICS_DIR = '../survival-game/resources/graphics/'
BASE_SOUND_EFFECT_DIR = '../survival-game/resources/sound_effect/'
BASE_SOUNDTRACK_DIR = '../survival-game/resources/soundtrack/'

# Numeric
EPSILON = 0.1
