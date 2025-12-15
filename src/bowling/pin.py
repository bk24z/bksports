import pygame
from src.constants import *
from src.bowling.conversions import convert_game_to_screen_pos

class Pin:
    HEIGHT = 15
    DIAMETER = 4.75
    RADIUS = DIAMETER / 2
    WEIGHT = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit = False

    def on_hit(self):
        self.hit = True
        print(f"Pin hit at ({self.x}, {self.y})")