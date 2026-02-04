import pygame

from bksports.bowling.game import BowlingGame
from bksports.constants import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def main() -> None:
    running = True
    while running:
        bowling_game = BowlingGame(screen, clock)
        bowling_game.run()
        running = bowling_game.running
    pygame.quit()

if __name__ == "__main__":
    main()
