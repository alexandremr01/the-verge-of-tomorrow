import sys
import pygame as pg

from data.main import main

if __name__ == '__main__':
    game = Game()
    game.main()
    pg.quit()
    sys.exit()