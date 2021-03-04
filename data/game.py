from constants import FRAMES_PER_SECOND

class Game:
    """
    Main class of the game, handles highest level functions
    """
    def __init__(self):
        self.running = True

    def main(self):
        while self.running:
            pass
            # lag += game.clock.tick(FRAMES_PER_SECOND)
            # self.event_loop()
            # self.draw(lag/TIME_PER_UPDATE)
