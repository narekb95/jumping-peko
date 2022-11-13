import pygame
import time
from pygame import (K_LEFT, K_RIGHT, KEYDOWN, KEYUP, K_a, K_d, WINDOWRESIZED, MOUSEBUTTONUP)
import random

screenx = 600
screeny = 900

score = 0
last_visited_brick_index = -1

BRICK_WIDTH_RATIO = 4
BRICK_SPEED_RATIO = 8000
JUMP_HEIGHT_DIFF_RATIO = 100_000
JUMP_HEIGHT_INITIAL_RATIO = 500
BRICK_Y_DIST_RATIO = 0.19
BALL_HORIZONTAL_SPEED_RATIO = 1000

ball_y = screeny * 0.7
ball_x = screenx / 2

bricks = [
    (0, screeny * .8, screenx, 10)]

def restartGame():
    global gameended
    global buttons
    global ball_x
    global ball_y
    global bricks
    global score
    global last_visited_brick_index
    global speed_x
    speed_x = 0
    gameended = False
    buttons[0]['show']=False
    ball_y = screeny * 0.7
    ball_x = screenx/2
    bricks = [(0, screeny * .8, screenx, 10)]
    score = 0
    last_visited_brick_index = -1

buttons = [
    {
        'text': "Restart",
        'show': False,
        'rect': (screenx * 0.33, screeny * 0.25, screenx* 0.33, screenx*0.10),
        'center': (screenx/2, screeny*0.8),
        'action': restartGame
    }
]
def intersectsButton(pos, button):
    return pos[0] > button[0] and pos[0] < button[0] + button[2] and pos[1] > button[1] and pos[1] < button[1] + button[3]

def handleClick(pos):
    print(pos)
    (x, y) = pos
    for button in buttons:
        (wdth, hght) = button['dim']
        (offsetx, offsety) = button['offset']
        print(offsetx, offsety, wdth, hght)
        if(button['show'] and intersectsButton((x,y), (offsetx, offsety, wdth, hght))):
            print('in')
            button['action']()
        print('out')
            

def displayButtons(screen):
    game_over_font = pygame.font.SysFont('Comic Sans MS', 30)
    for button in buttons:
        if button['show']:
                button_text = game_over_font.render(button['text'], False, (255, 255, 255))
                wdth = button_text.get_width()
                hght = button_text.get_height()
                offsetx = button['center'][0] - wdth/2
                offsety = button['center'][1] - hght/2
                pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(offsetx, offsety, wdth, hght))
                screen.blit(button_text, (offsetx, offsety, wdth, hght))
                button['dim'] = (wdth, hght)
                button['offset'] = (offsetx, offsety)


def updateBricks():
    global BRICK_WIDTH_RATIO
    global bricks
    global screenx
    global screeny
    
    # this line computes the minimum y value over all bricks
    miny = min(list(map(lambda brick:brick[1], bricks)))

    if miny > screeny * BRICK_Y_DIST_RATIO:
        width = screenx / BRICK_WIDTH_RATIO
        bricks.append((random.uniform(0, screenx - width),
         miny - screeny * BRICK_Y_DIST_RATIO,
          width, 10))
    fallingSpeed = screeny / BRICK_SPEED_RATIO * (1+score/10)
    bricks = list(map(lambda brick:  (brick[0], brick[1] + fallingSpeed, brick[2], brick[3]), bricks))

def intersect_bricks(pos):
    for brick in bricks:
        if(pos[0] >= brick[0] and pos[0] <= brick[0] + brick[2]
        and pos[1] >= brick[1] and pos[1] <= brick[1] + brick[3]):
            return bricks.index(brick)
    return -1

pygame.init()
pygame.font.init()
score_font = pygame.font.SysFont('Arial', 30)
game_over_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode([screenx, screeny], pygame.RESIZABLE)
running = True
speed_x = 0
speed_y = 0.01
black = (0, 0, 0)
direction_up = False
up_dist = 0
gameended = False

while running:
    if gameended:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                handleClick(pygame.mouse.get_pos())
    else:
        score_text = score_font.render('Score: ' + str(score), False, (0, 0, 255))
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
            if event.type == WINDOWRESIZED:
                screenx = screen.get_width()
                screeny =  screen.get_height()
                restartGame()

        ball_x += speed_x
        ball_x %= screenx
        screen.fill((255, 255, 255))
        updateBricks()
        for x in bricks:
            pygame.draw.rect(screen, black, pygame.Rect(x))
        pygame.draw.circle(screen, (100, 100, 255), (ball_x, ball_y), 10)

        if speed_y < 0:
            ball_y += speed_y 
        else:
            ball_y += speed_y * (1+score/10)
        speed_y += screeny / JUMP_HEIGHT_DIFF_RATIO

        brick_index = intersect_bricks((ball_x, ball_y))
        if speed_y > 0 and brick_index != -1:
            speed_y = - (screeny / JUMP_HEIGHT_INITIAL_RATIO)
            if brick_index > last_visited_brick_index:
                last_visited_brick_index = brick_index
                score += 1
        pygame.draw.rect(screen, (255,125,0),pygame.Rect(5,5,score_text.get_width(), score_text.get_height()))
        screen.blit(score_text, (5,5))
        displayButtons(screen)
        pygame.display.flip()

        if ball_y > screeny:
            gameended = True
            game_over_text = game_over_font.render('You are a looser haha!    Your score is '+str(score), False, (255, 255, 255))
            screen.fill(black)
            screen.blit(game_over_text, (screenx/2 - game_over_text.get_width()/2,screeny/2 - game_over_text.get_height()/2))
            buttons[0]['show']=True
            displayButtons(screen)
            pygame.display.flip()

pygame.quit()
