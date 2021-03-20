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

# Colors (RGB format)
ORANGE = (250, 157, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Map
CHUNK_SIZE = 500
CHUNK_ARRAY = np.array([CHUNK_SIZE, CHUNK_SIZE])
CHUNK_RECT = pygame.Rect((-CHUNK_SIZE/2, -CHUNK_SIZE/2), (CHUNK_SIZE, CHUNK_SIZE))
TOP_RECT = pygame.Rect((-CHUNK_SIZE/2, -CHUNK_SIZE/2), (CHUNK_SIZE, CHUNK_SIZE/3))
BOTTOM_RECT = pygame.Rect((-CHUNK_SIZE/2, -CHUNK_SIZE/2 + CHUNK_SIZE*2/3), (CHUNK_SIZE, CHUNK_SIZE/3))
LEFT_RECT = pygame.Rect((-CHUNK_SIZE/2, -CHUNK_SIZE/2), (CHUNK_SIZE/3, CHUNK_SIZE))
RIGHT_RECT = pygame.Rect((-CHUNK_SIZE/2 + CHUNK_SIZE*2/3, -CHUNK_SIZE/2), (CHUNK_SIZE/3, CHUNK_SIZE))
COORDINATES_TO_PIXEL_RATIO = 5
TILE_SIZE = 5
TILE_ARRAY = np.array([TILE_SIZE, TILE_SIZE])
MAX_OBJECT_COUNT = 100

# Waves
ENEMIES_INCREMENT_PER_WAVE = 10
TIME_TO_SPAWN = 5*1000  # milliseconds

# Enemies
SPAWN_DISTANCE = 100
DESPAWN_DISTANCE = 200
DEFAULT_ENEMY_VELOCITY = 2
DEFAULT_ENEMY_HEALTH = 100
ZOMBIE_VELOCITY = 3
ZOMBIE_HEALTH = 110

# Player
PLAYER_INITIAL_HEALTH = 10
PLAYER_INITIAL_VELOCITY = 5

# Bullet
BULLET_VELOCITY = 10

# Directories
BASE_GRAPHICS_DIR = '../survival-game/resources/graphics/'

# Numeric
EPSILON = 0.1
