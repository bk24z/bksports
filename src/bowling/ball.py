import math
from enum import Enum, auto

import src.constants as consts


class BallState(Enum):
    STATIONARY = auto()
    MID_THROW = auto()
    MOVING_IN_LANE = auto()
    OUT_OF_BOUNDS = auto()
    IN_LEFT_GUTTER = auto()
    IN_RIGHT_GUTTER = auto()
    FINISHED = auto()


class Ball:
    """
    Represents a bowling ball and its attributes,
    including its physics, position, and state within the game space.

    :ivar WEIGHT: The weight of the ball (currently undefined).
    :ivar DIAMETER: The diameter of the ball.
    :ivar RADIUS: The radius of the ball, derived from its diameter.
    :ivar CIRCUMFERENCE: The circumference of the ball, derived from its radius.
    :ivar x: The x-coordinate of the ball's position.
    :ivar y: The y-coordinate of the ball's position.
    :ivar vx: The velocity of the ball along the x-axis.
    :ivar vy: The velocity of the ball along the y-axis.
    :ivar state: The current state of the ball, which is an instance of the `BallState` enum.
    """

    WEIGHT = None  # TODO: Change value when needed
    DIAMETER = 8.5
    RADIUS = DIAMETER / 2
    CIRCUMFERENCE = 2 * math.pi * RADIUS

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.state = BallState.STATIONARY

    def throw(self, angle: float, velocity: float) -> None:
        """
        Throw the ball in the given direction with the given velocity.

        :param angle: The angle in degrees the ball is thrown at, relative to the vertical.
        :param velocity: The velocity of the ball in inches per second.
        """
        self.state = BallState.MID_THROW
        self.vx = velocity * math.sin(math.radians(angle))
        self.vy = velocity * math.cos(math.radians(angle))
        if False:  # If the ball is thrown behind, ...
            return
        self.state = BallState.MOVING_IN_LANE

    def update(self, dt: float) -> None:
        """
        Update the ball's position based on its velocity and time elapsed.

        :param dt: Time elapsed since the last update, in seconds.
        """
        is_moving_in_lane = self.state == BallState.MOVING_IN_LANE
        has_entered_left_gutter = self.x < consts.LEFT_BOUNDARY - consts.GUTTER_WIDTH / 2
        has_entered_right_gutter = self.x > consts.RIGHT_BOUNDARY + consts.GUTTER_WIDTH / 2
        has_entered_gutter = has_entered_left_gutter or has_entered_right_gutter
        is_finished = self.state == BallState.FINISHED
        in_gutter = self.state == BallState.IN_LEFT_GUTTER or self.state == BallState.IN_RIGHT_GUTTER
        if is_moving_in_lane:
            self.x += self.vx * dt
            self.y += self.vy * dt
            if self.y > consts.LANE_LENGTH:  # When the ball reaches the top of the lane, stop it
                self.state = BallState.FINISHED
                self.y = consts.LANE_LENGTH
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
            if self.y > consts.LANE_LENGTH:  # When the ball reaches the top of the lane, stop it
                self.state = BallState.FINISHED
                self.y = consts.LANE_LENGTH
