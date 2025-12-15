from src.constants import *


def convert_game_to_screen_pos(game_x, game_y, offset_x=0.0, offset_y=0.0):
    screen_x = SCREEN_WIDTH / 2 + (game_x * (ALLEY_SCREEN_WIDTH / LANE_WIDTH)) + offset_x
    screen_y = ALLEY_SCREEN_HEIGHT - (game_y * (ALLEY_SCREEN_HEIGHT / LANE_LENGTH)) + offset_y
    return screen_x, screen_y
