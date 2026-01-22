import math

import src.constants as consts
from src.bowling.ball import Ball


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
    HEIGHT = 15
    DIAMETER = 4.75
    RADIUS = DIAMETER / 2
    WEIGHT = None

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.hit = False

    def on_hit(self):
        self.hit = True
        print(f"Pin hit at ({self.x}, {self.y})")


class PinSet:
    """
    Represents a set of bowling pins arranged in a standard triangular formation.

    It defines their positions and determines when they are hit by the bowling ball.

    :ivar pins: List of pins in the pin set. Each pin's state and position are managed individually.
    :ivar pins_hit: Stores the number of pins the ball hit in the current throw.
    """

    def __init__(self):
        """
        Initialises the set of pins to their default state (not being hit) and position.
        """
        h = consts.HALF_PIN_SPACING_H
        v = consts.PIN_SPACING_V
        base_y = consts.FOUL_LINE_TO_FRONT_PIN_DISTANCE
        self.pins = [
            Pin(-h * 3, base_y + v * 3), Pin(-h, base_y + v * 3), Pin(h, base_y + v * 3), Pin(h * 3, base_y + v * 3),
            Pin(-h * 2, base_y + v * 2), Pin(0, base_y + v * 2), Pin(h * 2, base_y + v * 2),
            Pin(-h, base_y + v), Pin(h, base_y + v),
            Pin(0, base_y),
        ]
        self.pins_hit = 0

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
