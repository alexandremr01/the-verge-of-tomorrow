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
LOADBAR_WIDTH = 500
LOADBAR_HEIGHT = 5
SCREEN_ARRAY = np.array([SCREEN_WIDTH, SCREEN_HEIGHT])
PLAY_TO_OVER_DELAY = 5  # in frames
LOADING_TIME = 100  # in frames
GRAY_PAUSE_INTENSITY = 150
MANUAL_SCREEN_INPUT_LAG = 1*350  # milliseconds

# Colors (RGB format)
ORANGE = (250, 157, 0)
RED = (255, 0, 0)
BUTTON_RED = (170, 15, 15)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Title Screen
TITLE_FRAMERATE = 150
TITLE_MESSAGE_FRAMERATE = 500

# Map
RENDER_STEPS = 48
TILE_SIZE = 50
TILE_ARRAY = np.array([TILE_SIZE, TILE_SIZE])
TILE_NUMBER = 6 * 8  # Needs to be multiple of 6
CHUNK_SIZE = TILE_SIZE * TILE_NUMBER
CHUNK_ARRAY = np.array([CHUNK_SIZE, CHUNK_SIZE])
CHUNK_TILE_RATIO_STEPS = CHUNK_SIZE // TILE_SIZE // RENDER_STEPS


# Waves
ENEMIES_INCREMENT_PER_WAVE = 3
TIME_TO_SPAWN = 5*1000  # milliseconds
DAY_WAVE_DURATION = 30*1000
NIGHT_WAVE_DURATION = 10*1000
SHOW_WAVE_TIME = 2*1000

BATS_ROUND_PROBABILITY = 0.2
BATS_ROUND_TIME_TO_SPAWN_FACTOR = 3
NIGHT_PROBABILITY = 0.4
TIME_TO_SPAWN_SCHEDULE = 0.9
NIGHT_SCHEDULE = 1.1

ZOMBIE_PROB = 0.6
BAT_PROB = 0.4

ZOMBIE_PROB_AFTER = 0.4
BAT_PROB_AFTER = 0.3

GIANTS_APPEAR_ROUND = 4
NIGHTS_APPEAR_ROUND = 2
BATS_ROUNDS_APPEAR = 3

# Enemies
SPAWN_DISTANCE = 600
DESPAWN_DISTANCE = 800
DEFAULT_ENEMY_VELOCITY = 2
DEFAULT_ENEMY_HEALTH = 100
DEFAULT_ENEMY_DAMAGE = 1
PREDICTION_STEP = 5
ATTRACTION_FACTOR = 800
REPULSION_FACTOR = 75
ENEMY_VISION_RANGE = 10
VALID_POS_SEARCH_STEP = 15  # degrees

ZOMBIE_VELOCITY = 2
ZOMBIE_HEALTH = 110
ZOMBIE_DAMAGE = 1
ZOMBIE_SCORE = 5
ZOMBIE_NOISE_INTERVAL = 5000  # milliseconds

BAT_VELOCITY = 3
BAT_HEALTH = 70
BAT_DAMAGE = 0.5
BAT_SCORE = 3
BAT_WING_FREQUENCY = 3
BAT_NOISE_INTERVAL = 5000 # milliseconds
FRAMES_TO_ENEMIES_TURN = 3

GIANT_VELOCITY = 1
GIANT_HEALTH = 350
GIANT_DAMAGE = 2
GIANT_SCORE = 20
GIANT_NOISE_INTERVAL = 5000  # milliseconds


# Player
PLAYER_INITIAL_HEALTH = 5
PLAYER_INITIAL_VELOCITY = 15
PLAYER_HEAR_DISTANCE = 500  # in pixels
TIME_BETWEEN_COLLISIONS = 2*1000   # milliseconds
TIME_BETWEEN_HEARTBEAT = 2*1000  # milliseconds

# Bullet
BULLET_VELOCITY = 10

# Directories
BASE_GRAPHICS_DIR = '../the-verge-of-tomorrow/resources/graphics/'
BASE_SOUND_EFFECT_DIR = '../the-verge-of-tomorrow/resources/sound_effect/'
BASE_SOUNDTRACK_DIR = '../the-verge-of-tomorrow/resources/soundtrack/'
BASE_FONT_DIR = '../the-verge-of-tomorrow/resources/fonts/'

# Numeric
EPSILON = 0.1
