import math
from enum import Enum, auto

import pymunk

import bksports.constants as consts
from bksports.bowling.ball import Ball


class PinState(Enum):
    STANDING = auto()
    FALLING = auto()
    KNOCKED = auto()


class Pin:
    """
    Represents a bowling pin and its attributes.

    :ivar HEIGHT: The height of the pin.
    :ivar DIAMETER: The diameter of the pin.
    :ivar RADIUS: The radius of the pin, derived from its diameter.
    :ivar WEIGHT: The weight of the pin (currently undefined).
    :ivar x: The x-coordinate of the pin's position.
    :ivar y: The y-coordinate of the pin's position.
    :ivar hit: Indicates whether the pin has been hit.
    """

    HEIGHT = 15  # inches
    DIAMETER = 4.75  # inches
    RADIUS = DIAMETER / 2  # inches
    MASS = 1.55  # kg

    def __init__(self, x: float, y: float) -> None:
        self.removed = False
        self.body = pymunk.Body()
        self.body.position = (x, y)
        self.shape = pymunk.Circle(self.body, self.RADIUS)
        self.shape.mass = self.MASS
        self.shape.collision_type = (
            12  # Correct collision type has not been assigned yet
        )

    @property
    def x(self) -> float:
        return self.shape.body.position.x

    @property
    def y(self) -> float:
        return self.shape.body.position.y

    @property
    def vx(self) -> float:
        return self.shape.body.velocity.x

    @property
    def vy(self) -> float:
        return self.shape.body.velocity.y

    @property
    def hit(self) -> bool:
        return self.shape.collision_type == consts.HIT_PIN_ID

    def on_hit(self, arbiter, space, data) -> bool:  # noqa: ANN001
        self.shape.collision_type = consts.HIT_PIN_ID  # Signifies that the pin has already been hit, collision detection no longer needed
        print(f"Pin hit at ({self.x}, {self.y})")
        return True


class PinSet:
    """
    Represents a set of bowling pins arranged in a standard triangular formation.

    It defines their positions and determines when they are hit by the bowling ball.

    :ivar space: References the pymunk Space the game exists in.
    :ivar pins_hit: Stores the number of pins the ball hit in the current throw.
    :ivar pins: List of pins in the pin set. Each pin's state and position are managed individually.
    """

    def __init__(self, space: pymunk.Space) -> None:
        """Initialises the set of pins to their default state (not being hit) and position."""
        # Initialise other variables
        self.space = space
        self.pins_hit = 0
        # Reference constants
        h = consts.HALF_PIN_SPACING_H
        v = consts.PIN_SPACING_V
        base_y = consts.FOUL_LINE_TO_FRONT_PIN_DISTANCE
        # Intialise pins
        self.pins = [
            # First row
            Pin(-h * 3, base_y + v * 3),
            Pin(-h, base_y + v * 3),
            Pin(h, base_y + v * 3),
            Pin(h * 3, base_y + v * 3),
            # Second row
            Pin(-h * 2, base_y + v * 2),
            Pin(0, base_y + v * 2),
            Pin(h * 2, base_y + v * 2),
            # Third row
            Pin(-h, base_y + v),
            Pin(h, base_y + v),
            # Fourth row
            Pin(0, base_y),
        ]
        # Add pins' bodies and shapes to the space
        for i, pin in enumerate(self.pins, start=1):
            # Assign collision type IDs 1 to 10 to each pin
            pin.shape.collision_type = i
            # Intialise collision handlers for each pin
            self.space.on_collision(  # When the ball hits a pin that has not been hit by the ball
                collision_type_a=consts.BALL_ID,
                collision_type_b=i,
                separate=self.pins[i - 1].on_hit,
            )
            self.space.on_collision(  # When a pin that has been hit already hits another pin in a chain reaction
                collision_type_a=consts.HIT_PIN_ID,
                collision_type_b=i,
                separate=self.pins[i - 1].on_hit,
            )
            # Add each pin's body and shape to the space
            self.space.add(pin.body, pin.shape)

    def update(self, ball: Ball) -> None:
        """
        Updates the state of the pins based on the position of the ball.

        Pins that are hit by the ball within a specific radius are marked as hit.

        :param ball: The ball object whose position and radius are used to check for collisions with the pins.
        """
        for pin in self.pins:
            if pin.hit:
                continue
            ball_pin_distance = math.sqrt((ball.x - pin.x) ** 2 + (ball.y - pin.y) ** 2)
            if ball_pin_distance < Pin.RADIUS + Ball.RADIUS:
                pin.on_hit()
                self.pins_hit += 1

    def clean_up(self) -> None:
        for pin in self.pins:
            if pin.hit:
                pin.removed = True
