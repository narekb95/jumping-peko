import pygame
import time
from pygame import (K_LEFT, K_RIGHT, KEYDOWN, KEYUP, K_a, K_d)
import random

screenx = 600
screeny = 800

BRICK_WIDTH_RATIO = 4
BRICK_SPEED_RATIO = 8000
JUMP_HEIGHT_DIFF_RATIO = 100_000
JUMP_HEIGHT_INITIAL_RATIO = 500
BRICK_Y_DIST_RATIO = 0.15
BALL_HORIZONTAL_SPEED_RATIO = 1000

ball_y = screeny * 0.7
ball_x = screenx / 2

bricks = [
    (0, screeny * .8, screenx, 10)]
def updateBricks():
    global BRICK_WIDTH_RATIO
    global bricks
    global screenx
    global screeny
    miny = min(list(map(lambda brick:brick[1], bricks)))
    if miny > screeny * BRICK_Y_DIST_RATIO:
        width = screenx / BRICK_WIDTH_RATIO
        bricks.append((random.uniform(0, screenx - width), miny - screeny * BRICK_Y_DIST_RATIO, width, 10))
    bricks = list(map(lambda brick:  (brick[0], brick[1] + screeny / BRICK_SPEED_RATIO, brick[2], brick[3]), bricks))

def intersect_bricks(pos):
    for brick in bricks:
        if(pos[0] >= brick[0] and pos[0] <= brick[0] + brick[2]
        and pos[1] >= brick[1] and pos[1] <= brick[1] + brick[3]):
            return True
    return False

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
game_over_text = my_font.render('You have lost bitch', False, (255, 255, 255))

screen = pygame.display.set_mode([screenx, screeny])
running = True
speed_x = 0
speed_y = 0.01
black = (0, 0, 0)
direction_up = False
up_dist = 0
lost = False

while running:
    time.sleep(0.001)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                speed_x -= (screenx / BALL_HORIZONTAL_SPEED_RATIO)
            if event.key == K_RIGHT or event.key == K_d:
                speed_x += screenx / BALL_HORIZONTAL_SPEED_RATIO
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_a:
                speed_x += (screenx / BALL_HORIZONTAL_SPEED_RATIO)
            if event.key == K_RIGHT or event.key == K_d:
                speed_x -= screenx / BALL_HORIZONTAL_SPEED_RATIO
        if event.type == pygame.QUIT:
            running = False

    ball_x += speed_x
    ball_x %= screenx
    screen.fill((255, 255, 255))
    updateBricks()
    for x in bricks:
        pygame.draw.rect(screen, black, pygame.Rect(x))
    pygame.draw.circle(screen, (100, 100, 255), (ball_x, ball_y), 10)

    ball_y += speed_y
    speed_y += screeny / JUMP_HEIGHT_DIFF_RATIO
    if speed_y > 0 and intersect_bricks((ball_x, ball_y)):
        speed_y = - (screeny / JUMP_HEIGHT_INITIAL_RATIO)
    pygame.display.flip()

    if ball_y > screeny:
        screen.fill(black)
        screen.blit(game_over_text, (screenx/2 - game_over_text.get_width()/2,screeny/2 - game_over_text.get_height()/2))
        pygame.display.flip()
        time.sleep(2)
        lost = False    
        ball_y = screeny * 0.7
        ball_x = screenx/2
        bricks = [(0, screeny * .8, screenx, 10)]

pygame.quit()