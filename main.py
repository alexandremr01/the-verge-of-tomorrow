"""
Root file, calls the main from Game class
"""

import sys
import pygame
from data.game import Game

pygame.init()

game = Game()
game.main()

pygame.quit()
sys.exit()
