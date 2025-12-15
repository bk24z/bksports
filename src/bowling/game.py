import math
import pygame

from src.constants import *

from src.bowling.ball import *
from src.bowling.pin import Pin
from src.bowling.trajectory import TrajectoryLine
from src.bowling.conversions import convert_game_to_screen_pos

# background = pygame.image.load('../../assets/background.jpg')

def initialise_pins():
    h = HALF_PIN_SPACING_H
    v = PIN_SPACING_V
    base_y = FOUL_LINE_TO_FRONT_PIN_DISTANCE
    return [
        Pin(-h * 3, base_y + v * 3), Pin(-h, base_y + v * 3), Pin(h, base_y + v * 3), Pin(h * 3, base_y + v * 3),
        Pin(-h * 2, base_y + v * 2), Pin(0, base_y + v * 2), Pin(h * 2, base_y + v * 2),
        Pin(-h, base_y + v), Pin(h, base_y + v),
        Pin(0, base_y),
    ]

def setup_bowling_scene(screen):
    # Fill the screen with a white background
    screen.fill(WHITE)

    # Calculate the alley and gutter dimensions
    left_boundary_x, _ = convert_game_to_screen_pos(LEFT_BOUNDARY, 0)
    right_boundary_x, _ = convert_game_to_screen_pos(RIGHT_BOUNDARY, 0)
    left_gutter_x, _ = convert_game_to_screen_pos(LEFT_BOUNDARY - GUTTER_WIDTH, 0)
    right_gutter_x, _ = convert_game_to_screen_pos(RIGHT_BOUNDARY, 0)
    gutter_width = GUTTER_WIDTH * (ALLEY_SCREEN_WIDTH / LANE_WIDTH)

    # Draw the alley
    pygame.draw.rect(screen, BUTCHER_BLOCK,
                     pygame.Rect(left_boundary_x, 0, ALLEY_SCREEN_WIDTH, ALLEY_SCREEN_HEIGHT))

    # Draw the left gutter
    pygame.draw.rect(screen, BLACK,
                     pygame.Rect(left_gutter_x, 0, gutter_width, ALLEY_SCREEN_HEIGHT))

    # Draw the right gutter
    pygame.draw.rect(screen, BLACK,
                     pygame.Rect(right_gutter_x, 0, gutter_width, ALLEY_SCREEN_HEIGHT))


BALL_SCREEN_RADIUS = Ball.RADIUS * (ALLEY_SCREEN_WIDTH / LANE_WIDTH)
BALL_SCREEN_WIDTH = BALL_SCREEN_RADIUS * 2
BALL_SCREEN_HEIGHT = BALL_SCREEN_RADIUS * 2

PIN_SCREEN_RADIUS = Pin.RADIUS * (ALLEY_SCREEN_WIDTH / LANE_WIDTH)
PIN_SCREEN_WIDTH = PIN_SCREEN_RADIUS * 2
PIN_SCREEN_HEIGHT = PIN_SCREEN_RADIUS * 2

class BowlingGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.ball = Ball()
        self.ball_angle = 0
        self.pins = initialise_pins()
        self.trajectory_line = TrajectoryLine(self.ball, self.screen, self.ball_angle)
        self.running = True

    def display_ball(self):
        # print(f"Ball game pos: ({self.ball.x}, {self.ball.y})")
        x, y = convert_game_to_screen_pos(self.ball.x, self.ball.y)
        # print(f"Ball screen pos: ({self.x}, {self.y})")
        # screen.blit(self.img, (self.x, self.y))
        pygame.draw.circle(self.screen, LIGHT_BLUE, (x, y), BALL_SCREEN_RADIUS)

    def change_ball_angle(self, angle):
        new_angle = self.ball_angle + angle
        if -5 <= new_angle <= 5:
            self.ball_angle = new_angle
            self.trajectory_line.angle = self.ball_angle
            self.trajectory_line.calculate_pos()
        # self.ball_angle += angle
        # self.ball.change_angle(angle)
        # self.trajectory_line.angle = self.ball_angle
        # self.trajectory_line.change_angle(angle)
        print(self.ball_angle)
        print(self.trajectory_line.angle)

    def throw_ball(self, velocity):
        self.ball.throw(self.ball_angle, velocity)

    def display_pins(self):
        for pin in self.pins:
            x, y = convert_game_to_screen_pos(pin.x, pin.y)
            color = RED if pin.hit else BLACK
            pygame.draw.circle(self.screen, color, (x, y), PIN_SCREEN_RADIUS)

    def update_pins(self):
        for pin in self.pins:
            x, y = convert_game_to_screen_pos(pin.x, pin.y)
            color = RED if pin.hit else BLACK
            pygame.draw.circle(self.screen, color, (x, y), PIN_SCREEN_RADIUS)
            if pin.hit:
                continue
            ball_pin_distance = math.sqrt((self.ball.x - pin.x) ** 2 + (self.ball.y - pin.y) ** 2)
            # print(f"Ball-pin distance: {ball_pin_distance}")
            if ball_pin_distance < Pin.RADIUS + Ball.RADIUS:
                pin.on_hit()

    def end_frame(self):
        pins_hit = len([1 for pin in self.pins if pin.hit])
        print(f"Finished! Pins hit: {pins_hit}")
        self.ball.__init__()  # Reset ball
        pins = initialise_pins()
        return pins

    def run(self):
        while self.running:
            setup_bowling_scene(self.screen)

            # Display the background image
            # screen.blit(background, (0, 0))

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.throw(self.ball_angle, 317)
                    if event.key == pygame.K_LEFT:
                        self.change_ball_angle(-0.5)
                    if event.key == pygame.K_RIGHT:
                        self.change_ball_angle(0.5)
            if self.ball.state == BallState.STATIONARY:
                self.trajectory_line.display()
            if self.ball.state == BallState.FINISHED:
                pins = self.end_frame()
            self.display_ball()
            self.update_pins()
            pygame.display.update()
            dt = self.clock.tick(FRAMES_PER_SECOND) / 1000.0  # Limits FPS to 60, dt is time in seconds since the last frame
            self.ball.update(dt)