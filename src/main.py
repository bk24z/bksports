import pygame
import time
import math

from constants import *
from src.bowling.game import BowlingGame

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def main():
    running = True
    while running:
        bowling_game = BowlingGame(screen, clock)
        bowling_game.run()
        running = bowling_game.running

if __name__ == "__main__":
    main()
