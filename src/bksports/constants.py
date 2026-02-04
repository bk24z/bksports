"""
General constants, and constants for bowling alley physics and rendering.

All physical/game measurements for the bowling game (lane, ball, pin dimensions) use inches to align
with bowling industry standards. Screen dimensions are in pixels.
"""

FRAMES_PER_SECOND = 60

### GENERAL CONSTANTS ###

# === Screen Dimensions (pixels) ===

SCREEN_WIDTH = 720  # TODO: Change once final screen size is determined
SCREEN_HEIGHT = 1024 - 32  # TODO: Change once final screen size is determined

# === Colours (RGB) ===

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
BUTCHER_BLOCK = (190, 172, 76)  # Bowling lane colour

### BOWLING CONSTANTS ###

# === Physical Measurements (inches) ===
# Based on USBC (United States Bowling Congress) specifications

# Lane dimensions
LANE_WIDTH = 41.5  # Width of the lane
GUTTER_WIDTH = 9.25  # Width of each gutter
ALLEY_WIDTH = LANE_WIDTH + GUTTER_WIDTH * 2  # Total width of the alley
LANE_LENGTH = 65 * 12  # Distance from foul line to end of lane (65 feet?) TODO: Needs to be checked
APPROACH_LENGTH = 15 * 12  # Distance of approach, start of lane to foul lane (15 feet) TODO: Needs to be checked

# Lane boundaries (x-coordinates from the centre of alley)
LEFT_BOUNDARY = -(LANE_WIDTH / 2)
RIGHT_BOUNDARY = (LANE_WIDTH / 2)

# Pin positioning
FOUL_LINE_TO_FRONT_PIN_DISTANCE = 60 * 12  # Distance from the foul line to the first pin at the front (60 feet) TODO: Needs to be checked
FOUL_LINE_TO_END_DISTANCE = None  # Distance from the foul line to the end of the lane (? feet) TODO: Find correct value and change this
PIN_SPACING_H = 12  # Centre to centre distance
HALF_PIN_SPACING_H = PIN_SPACING_H / 2  # TODO: Change back to PIN_SPACING_H after testing
PIN_SPACING_V = 20.75 / 2  # Spacing between rows of pins TODO: Change back to 20.75 after testing

# === Bowling Screen Dimensions (pixels) ===

ALLEY_SCREEN_HEIGHT = SCREEN_HEIGHT
ALLEY_SCREEN_WIDTH = ALLEY_SCREEN_HEIGHT * (LANE_WIDTH / LANE_LENGTH)  # Aspect ratio maintained

# === Pymunk Constants ===
BALL_ID = 0
HIT_PIN_ID = 11
