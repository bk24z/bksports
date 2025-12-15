import pygame
import math
from enum import Enum, auto

from src.constants import *
from src.bowling.conversions import convert_game_to_screen_pos


class BallState(Enum):
    STATIONARY = auto()
    MID_THROW = auto()
    MOVING_IN_LANE = auto()
    OUT_OF_BOUNDS = auto()
    IN_LEFT_GUTTER = auto()
    IN_RIGHT_GUTTER = auto()
    FINISHED = auto()


class Ball:
    """Game logic for the ball - physics, position, etc. in game space"""
    WEIGHT = None
    DIAMETER = 8.5
    RADIUS = DIAMETER / 2
    CIRCUMFERENCE = 2 * math.pi * RADIUS

    def __init__(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.state = BallState.STATIONARY

    def throw(self, angle, velocity):
        self.state = BallState.MID_THROW
        self.vx = velocity * math.sin(math.radians(angle))
        self.vy = velocity * math.cos(math.radians(angle))
        if False:  # If the ball is thrown behind, ...
            return
        self.state = BallState.MOVING_IN_LANE

    def update(self, dt):
        is_moving_in_lane = self.state == BallState.MOVING_IN_LANE
        has_entered_left_gutter = self.x < LEFT_BOUNDARY - GUTTER_WIDTH / 2
        has_entered_right_gutter = self.x > RIGHT_BOUNDARY + GUTTER_WIDTH / 2
        has_entered_gutter = has_entered_left_gutter or has_entered_right_gutter
        is_finished = self.state == BallState.FINISHED
        in_gutter = self.state == BallState.IN_LEFT_GUTTER or self.state == BallState.IN_RIGHT_GUTTER
        if is_moving_in_lane:
            self.x += self.vx * dt
            self.y += self.vy * dt
            if self.y > LANE_LENGTH:  # When the ball reaches the top of the lane, stop it
                self.state = BallState.FINISHED
                self.y = LANE_LENGTH
                # self.on_finish()
            if has_entered_gutter:  # If the ball goes into the gutter, ...
                print(f"GUTTER! x={self.x}")
                if has_entered_left_gutter:
                    self.state = BallState.IN_LEFT_GUTTER
                if has_entered_right_gutter:
                    self.state = BallState.IN_RIGHT_GUTTER
            if False:  # If the ball goes directly out of bounds, ...
                self.state = BallState.OUT_OF_BOUNDS
        if in_gutter:
            self.y += self.vy * dt  # Keep the ball moving vertically in the gutter
            if self.y > LANE_LENGTH:  # When the ball reaches the top of the lane, stop it
                self.state = BallState.FINISHED
                self.y = LANE_LENGTH
