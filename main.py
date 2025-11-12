import pygame
import time
import math
from enum import Enum, auto

pygame.init()

FRAMES_PER_SECOND = 60

# Measurements
# All lane, ball, pin measurements are in inches (to align with industry standards)
LANE_WIDTH = 41.5
GUTTER_WIDTH = 9.25
ALLEY_WIDTH = LANE_WIDTH + GUTTER_WIDTH * 2
LANE_LENGTH = 65 * 12  # 90 feet TODO: Needs to be checked
FOUL_LINE_TO_FRONT_PIN_DISTANCE = 60 * 12  # 60 feet
FOUL_LINE_TO_END_DISTANCE = None
APPROACH_LENGTH = 15 * 12  # 15 feet
LEFT_BOUNDARY = -(LANE_WIDTH / 2)
RIGHT_BOUNDARY = (LANE_WIDTH / 2)

PIN_SPACING_H = 12  # Spacing between centres of pins
HALF_PIN_SPACING_H = PIN_SPACING_H / 2
PIN_SPACING_V = 20.75 / 2

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen_width = 1280
screen_height = 720 * 1.2

# Dimensions
# 480p 9:16 to try and make the window have a similar aspect ratio to the game space alley
# screen_width = 480
# screen_height = 854
# screen_width = LANE_WIDTH * 5
# screen_height = LANE_LENGTH * 5

screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('assets/bowling-alley.jpg')
clock = pygame.time.Clock()

class BallState(Enum):
    STATIONARY = auto()
    MID_THROW = auto()
    MOVING_IN_LANE = auto()
    OUT_OF_BOUNDS = auto()
    IN_GUTTER = auto()
    FINISHED = auto()


class Ball:
    """Game logic for the ball - physics, position, etc. in game space"""
    WEIGHT = None
    RADIUS = 8.5 / 2  # ?
    DIAMETER = RADIUS * 2
    CIRCUMFERENCE = 2 * math.pi * RADIUS
    UPDATE_FREQUENCY = 100  # Updates every x seconds

    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.img = BallImage(self)
        self.state = BallState.STATIONARY

    def throw(self, angle, velocity):
        self.state = BallState.MID_THROW
        self.vx = velocity * math.sin(math.radians(angle))
        self.vy = velocity * math.cos(math.radians(angle))
        if False:  # If the ball is thrown behind, ...
            return
        self.state = BallState.MOVING_IN_LANE

    def update(self, dt):
        if self.state == BallState.MOVING_IN_LANE:
            self.x += self.vx * dt
            self.y += self.vy * dt
            if self.y > LANE_LENGTH:  # When the ball reaches the top of the lane, stop it
                self.state = BallState.FINISHED
                self.y = LANE_LENGTH
            if self.x < LEFT_BOUNDARY or self.x > RIGHT_BOUNDARY:  # If the ball goes into the gutter, ...
                print(f"GUTTER! x={self.x}")
                self.state = BallState.IN_GUTTER
            if False:  # If the ball goes directly out of bounds, ...
                self.state = BallState.OUT_OF_BOUNDS
            # for pin in PINS:
            #     if False:  # If the ball hits a pin, ...
            #         pass
            print(self.x, self.y)
        # self.img.calculate_pos()



class BallImage:
    """Represents the ball's image, which is displayed on the screen, corresponding to self.ball's co-ordinates."""

    def __init__(self, ball):
        self.ball = ball
        self.img = pygame.image.load('assets/ball_blue_large.png')
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = (screen_width / 2) - (self.width / 2)
        self.y = screen_height - (self.height / 2)

    def display(self):
        print(f"Ball game pos: ({self.ball.x}, {self.ball.y})")
        self.x, self.y = convert_game_to_screen_pos(self.ball.x, self.ball.y, offset_x=-self.width / 2,
                                                    offset_y=-self.height / 2)
        print(f"Ball screen pos: ({self.x}, {self.y})")
        screen.blit(self.img, (self.x, self.y))


class TrajectoryLine:
    """Represents the trajectory line, which is a line that shows the ball's predicted trajectory."""

    LENGTH = 500

    def __init__(self, ball):
        self.ball = ball
        self.start_pos = None
        self.end_pos = None
        self.__angle = 0
        self.calculate_pos()

    def change_angle(self, angle):
        new_angle = self.__angle + angle
        if -5 <= new_angle <= 5:
            self.__angle = new_angle
            print(self.__angle)
            self.calculate_pos()

    def get_angle(self):
        return self.__angle

    def calculate_pos(self):
        start_x = self.ball.x
        start_y = self.ball.y
        self.start_pos = convert_game_to_screen_pos(start_x, start_y)
        end_x = self.ball.x + self.LENGTH * math.sin(math.radians(self.__angle))
        end_y = self.ball.y + self.LENGTH * math.cos(math.radians(self.__angle))
        self.end_pos = convert_game_to_screen_pos(end_x, end_y)
        print(f"Angle: {self.__angle}, end_y (game): {end_y}, end_pos (screen): {self.end_pos}")

    def display(self):
        pygame.draw.line(screen, (255, 0, 0), self.start_pos, self.end_pos, 5)


class Pin:
    HEIGHT = 15
    RADIUS = 1
    DIAMETER = RADIUS * 2
    WEIGHT = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = PinImage(self)

    def hit(self):
        self.img.color = RED


class PinImage:
    def __init__(self, pin, x=None, y=None):
        self.pin = pin
        self.color = BLACK
        self.x = x
        self.y = y

    def display(self):
        self.x, self.y = convert_game_to_screen_pos(self.pin.x, self.pin.y)
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)


def convert_game_to_screen_pos(game_x, game_y, offset_x=0.0, offset_y=0.0):
    screen_x = (screen_width / 2) + (game_x * (screen_width / LANE_WIDTH)) + offset_x
    screen_y = screen_height - (game_y * (screen_height / LANE_LENGTH)) + offset_y
    return screen_x, screen_y

def main():
    ball = Ball()
    trajectory_line = TrajectoryLine(ball)
    h = HALF_PIN_SPACING_H
    v = PIN_SPACING_V
    base_y = FOUL_LINE_TO_FRONT_PIN_DISTANCE
    # pins = [
    #     Pin(-h*2, base_y + v*2), Pin(6, FOUL_LINE_TO_FRONT_PIN_DISTANCE + PIN_SPACING_V * 2), Pin(HALF_PIN_SPACING_H * 2, FOUL_LINE_TO_FRONT_PIN_DISTANCE + PIN_SPACING_V * 2),
    #     Pin(-HALF_PIN_SPACING_H, FOUL_LINE_TO_FRONT_PIN_DISTANCE + (20.75 / 2)), Pin(HALF_PIN_SPACING_H, FOUL_LINE_TO_FRONT_PIN_DISTANCE + (20.75 / 2)),
    #     Pin(0, FOUL_LINE_TO_FRONT_PIN_DISTANCE),
    # ]
    pins = [
        Pin(-h * 3, base_y + v * 3), Pin(-h, base_y + v * 3), Pin(h, base_y + v * 3), Pin(h * 3, base_y + v * 3),
        Pin(-h * 2, base_y + v * 2), Pin(0, base_y + v * 2), Pin(h * 2, base_y + v * 2),
        Pin(-h, base_y + v), Pin(h, base_y + v),
        Pin(0, base_y),
    ]
    running = True
    while running:
        screen.fill((255, 255, 255))
        # screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball.throw(trajectory_line.get_angle(), 317)
                if event.key == pygame.K_LEFT:
                    trajectory_line.change_angle(-0.5)
                if event.key == pygame.K_RIGHT:
                    trajectory_line.change_angle(0.5)
        if ball.state == BallState.STATIONARY:
            trajectory_line.display()
        ball.img.display()
        for pin in pins:
            pin.img.display()
        pygame.display.update()
        dt = clock.tick(FRAMES_PER_SECOND) / 1000.0  # Limits FPS to 60, dt is time in seconds since the last frame
        ball.update(dt)


if __name__ == "__main__":
    main()
