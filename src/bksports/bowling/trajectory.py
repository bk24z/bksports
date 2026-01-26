import pygame
import math

from bksports.bowling.conversions import convert_game_to_screen_pos


class TrajectoryLine:
    """Represents the trajectory line, which is a line that shows the ball's predicted trajectory."""

    LENGTH = 400

    def __init__(self, ball, screen, angle):
        self.ball = ball
        self.screen = screen
        self.angle = angle
        self.start_pos = None
        self.end_pos = None
        # self.start_pos, self.end_pos =
        self.calculate_pos()

    def change_angle(self, angle):
        new_angle = self.angle + angle
        if -5 <= new_angle <= 5:
            self.angle = new_angle
            print(self.angle)
            #self.start_pos, self.end_pos = (
            self.calculate_pos()

    def get_angle(self):
        return self.angle

    def calculate_pos(self):
        start_x = self.ball.x
        start_y = self.ball.y
        self.start_pos = convert_game_to_screen_pos(start_x, start_y)
        end_x = self.ball.x + self.LENGTH * math.sin(math.radians(self.angle))
        end_y = self.ball.y + self.LENGTH * math.cos(math.radians(self.angle))
        self.end_pos = convert_game_to_screen_pos(end_x, end_y)
        # print(f"Angle: {self.__angle}, end_y (game): {end_y}, end_pos (screen): {self.end_pos}")
        # return start_pos, end_pos

    def display(self):
        pygame.draw.line(self.screen, (255, 0, 0), self.start_pos, self.end_pos, 5)