from src.sports.constants import SCREEN_WIDTH, ALLEY_SCREEN_WIDTH, ALLEY_SCREEN_HEIGHT, LANE_WIDTH, LANE_LENGTH


def convert_game_to_screen_pos(
        game_x: float,
        game_y: float,
        offset_x: float = 0.0,
        offset_y: float = 0.0
) -> tuple[float, float]:
    """
    Converts a position in game coordinates (origin at the bottom centre of the alley, unit is inches)
    to the same position in screen coordinates (origin at the top left of the screen, unit is pixels).
    :param game_x: The game x-coordinate (horizontal position on lane).
    :param game_y: The game y-coordinate (distance down the lane).
    :param offset_x: The x-coordinate offset in pixels (if any).
    :param offset_y: The y-coordinate offset in pixels (if any).
    :return: A tuple (screen_x, screen_y) in screen (pixel) coordinates.
    """
    screen_x = SCREEN_WIDTH / 2 + (game_x * (ALLEY_SCREEN_WIDTH / LANE_WIDTH)) + offset_x
    screen_y = ALLEY_SCREEN_HEIGHT - (game_y * (ALLEY_SCREEN_HEIGHT / LANE_LENGTH)) + offset_y
    return screen_x, screen_y
