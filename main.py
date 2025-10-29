import pygame
import time
import math

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('assets/bowling-alley.jpg')
clock = pygame.time.Clock()

class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0

class BallImage:
    def __init__(self, ball):
        self.ball = ball
        self.img = pygame.transform.rotozoom(ball_img_original, 0, ball_scale)
        self.img_width = self.img.get_width()
        self.img_height = self.img.get_height()
        self.img_X = (screen_width / 2) - (self.img_width / 2)
        self.img_Y = 500
        self.img_X_change = 0
        self.img_Y_change = 0

class Trajectory:
    def __init__(self):
        self.angle = 0
        self.startpoint_x = ball_img_X + (ball_img_width / 2)
        self.startpoint_y = ball_img_Y
        endpoint_x = self.startpoint_x + 200 * math.sin(math.radians(self.angle))
        endpoint_y = self.startpoint_y - 200 * math.cos(math.radians(self.angle))
        self.endpoint = (endpoint_x, endpoint_y)
    def change_angle(self, angle):
        self.angle += angle

# Ball
ball_img_original = pygame.image.load('assets/ball_blue_small.png')
ball_scale = 1
ball_img = pygame.transform.rotozoom(ball_img_original, 0, ball_scale)
ball_img_width = ball_img.get_width()
ball_img_height = ball_img.get_height()
ball_img_X = (screen_width / 2) - (ball_img_width / 2)
ball_img_Y = 500
ball_img_X_change = 0
ball_img_Y_change = 0

trajectory_angle = 0
# trajectory_shift_X =

ballX = 0
ballY = 0

def ball(x,y):
    screen.blit(ball_img, (x, y))

def trajectory(x,y):
    pygame.draw.line(screen, (255, 0, 0), (ball_img_X+(ball_img_width/2), ball_img_Y), (x, y), 5)

running = True
ball_moving = False
frame_count = 0

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ball_moving = True
            if event.key == pygame.K_LEFT:
                trajectory_angle -= 10
            if event.key == pygame.K_RIGHT:
                trajectory_angle += 10
    if ball_moving and ball_img_Y >= 150:
        ball_img_Y_change = -5
        frame_count += 1
        if frame_count % 2 == 0:  # Only rescale every 10 frames
            ball_scale -= 0.02
            ball_img = pygame.transform.rotozoom(ball_img_original, 0, ball_scale)
    else:
        ball_img_Y_change = 0
    ball_img_Y += ball_img_Y_change
    ball(ball_img_X, ball_img_Y)
    # trajectory(
    #     ball_img_X+(ball_img_width/2),
    #     400
    # )
    if not ball_moving:
        trajectory_start_X = ball_img_X + (ball_img_width/2)
        trajectory_start_Y = ball_img_Y
        trajectory_length = 200  # Length of the trajectory line
        trajectory_endpoint_X = trajectory_start_X + trajectory_length * math.sin(math.radians(trajectory_angle))
        trajectory_endpoint_Y = trajectory_start_Y - trajectory_length * math.cos(math.radians(trajectory_angle))
        trajectory(
            trajectory_endpoint_X,
            trajectory_endpoint_Y
        )
    pygame.display.update()
    clock.tick(60)