# Atari pong
# By KyushikMin kyushikmin@gamil.com
# http://mmc.hanyang.ac.kr 

import random, sys, time, math, pygame
from pygame.locals import *
import numpy as np
import copy

# Window Information
FPS = 30 
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 360

HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int(WINDOW_HEIGHT / 2)

# Colors
#				 R    G    B
WHITE        = (255, 255, 255)
BLACK		 = (  0,   0,   0)
RED 		 = (200,  72,  72)
LIGHT_ORANGE = (198, 108,  58)
ORANGE       = (180, 122,  48)
GREEN		 = ( 72, 160,  72)
BLUE 		 = ( 66,  72, 200)
YELLOW 		 = (162, 162,  42)
NAVY         = ( 75,   0, 130)
PURPLE       = (143,   0, 255)

def main():
    global FPS_CLOCK, DISPLAYSURF, BASIC_FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption('Pong')
    # pygame.display.set_icon(pygame.image.load('./Qar_Sim/icon_resize2.png'))

    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 16)

    # Set initial parameters

    init = True
    my_score = 0
    enemy_score = 0

    my_bar_width = 10
    my_bar_height = 50
    my_bar_init_position = (WINDOW_HEIGHT - my_bar_height)/2
    my_bar_position = my_bar_init_position
    my_bar_speed = 5

    enemy_bar_width = 10
    enemy_bar_height = 100
    enemy_bar_init_position = (WINDOW_HEIGHT - enemy_bar_height)/2
    enemy_bar_position = enemy_bar_init_position
    enemy_bar_speed = 5

    ball_init_position_x = WINDOW_WIDTH / 2
    ball_init_position_y = WINDOW_HEIGHT / 2 

    ball_position_x = ball_init_position_x
    ball_position_y = ball_init_position_y

    ball_radius = 5

    random_start_x = random.randint(0, 1)
    random_start_y = random.randint(0, 1)

    if random_start_x == 0:
        ball_speed_x = - random.uniform(6.0, 9.0)
    else:
        ball_speed_x = random.uniform(6.0, 9.0)

    if random_start_y == 0:
        ball_speed_y = -random.uniform(6.0, 9.0)
    else:
        ball_speed_y = random.uniform(6.0, 9.0)


    direction = ''
    while True: # Game loop
        # Initial settings
        if init == True:
            my_bar_position = my_bar_init_position
            enemy_bar_init_position = WINDOW_HEIGHT - (enemy_bar_height/2)

            ball_position_x = ball_init_position_x
            ball_position_y = ball_init_position_y
            
            random_start_x = random.randint(0, 1)
            random_start_y = random.randint(0, 1)

            if random_start_x == 0:
                ball_speed_x = - random.uniform(6.0, 9.0)
            else:
                ball_speed_x = random.uniform(6.0, 9.0)

            if random_start_y == 0:
                ball_speed_y = -random.uniform(6.0, 9.0)
            else:
                ball_speed_y = random.uniform(6.0, 9.0)

            init = False

        # Key settings
        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_UP):
                    direction = 'UP' 
                elif (event.key == K_DOWN):
                    direction = 'DOWN' 
                elif event.key == K_ESCAPE:
                    terminate()
                else:
                    direction = 'HOLD'

        # Control the bar
        if direction == 'UP':
            my_bar_position -= my_bar_speed			
        elif direction == 'DOWN':
            my_bar_position += my_bar_speed

        # Constraint of the bar
        if my_bar_position <= 0:
            my_bar_position = 0

        if my_bar_position >= WINDOW_HEIGHT - my_bar_height:
            my_bar_position = WINDOW_HEIGHT - my_bar_height

        # Move the ball
        ball_position_x += ball_speed_x
        ball_position_y += ball_speed_y

        # Move the enemy
        enemy_bar_position = ball_position_y - (enemy_bar_height/2)

        # Constraint of enemy bar
        if enemy_bar_position <= 0:
            enemy_bar_position = 0

        if enemy_bar_position >= WINDOW_HEIGHT - enemy_bar_height:
            enemy_bar_position = WINDOW_HEIGHT - enemy_bar_height

        # Ball is bounced when the ball hit the wall
        if ball_position_y <= 0 or ball_position_y >= WINDOW_HEIGHT:
            ball_speed_y = - ball_speed_y
        
        # Ball is bounced when the ball hit the bar
        if ball_position_x <= my_bar_width:
            # Hit the ball!
            if ball_position_y <= my_bar_position + my_bar_height and ball_position_y >= my_bar_position:
                ball_position_x = my_bar_width + 1
                ball_speed_x = - ball_speed_x

                # When the ball is at the corner
                if ball_position_y >= WINDOW_HEIGHT:
                    ball_position_x = my_bar_width + 1
                    ball_position_y = WINDOW_HEIGHT -1 
                    ball_speed_x = - ball_speed_x
                    ball_speed_y = - ball_speed_y

                if ball_position_y <= 0:
                    ball_position_x = my_bar_width +1
                    ball_position_y = 1 
                    ball_speed_x = - ball_speed_x
                    ball_speed_y = - ball_speed_y               
        
        # Lose :( 
        if ball_position_x <= 0:
            enemy_score += 1
            
            if enemy_score > 10:
                enemy_score = 0
                my_score = 0

            init = True

        # The ball is bounced when enemy hit the ball
        if ball_position_x >= WINDOW_WIDTH - enemy_bar_width:
            # enemy hit the ball
            if ball_position_y <= enemy_bar_position + enemy_bar_height and ball_position_y >= enemy_bar_position:
                ball_position_x = WINDOW_WIDTH - enemy_bar_width - 1
                ball_speed_x = - ball_speed_x

                # When the ball is at the corner
                if ball_position_y >= WINDOW_HEIGHT:
                    ball_position_x = WINDOW_WIDTH - enemy_bar_width -1
                    ball_position_y = WINDOW_HEIGHT -1 
                    ball_speed_x = - ball_speed_x
                    ball_speed_y = - ball_speed_y

                if ball_position_y <= 0:
                    ball_position_x = WINDOW_WIDTH - enemy_bar_width -1
                    ball_position_y = 1 
                    ball_speed_x = - ball_speed_x
                    ball_speed_y = - ball_speed_y                

        # WIN!! :)
        if ball_position_x >= WINDOW_WIDTH:
            my_score += 1
           
            if my_score > 10:
                enemy_score = 0
                my_score = 0
            
            init = True 

        # Fill background color
        DISPLAYSURF.fill(BLACK)

        # Display scores
        score_msg(my_score, ((WINDOW_WIDTH/2) - 45, (WINDOW_HEIGHT/2)-10))
        score_msg(enemy_score, ((WINDOW_WIDTH/2) + 35, (WINDOW_HEIGHT/2)-10))

        # Draw bar
        my_bar_rect = pygame.Rect(0, my_bar_position, my_bar_width, my_bar_height)
        pygame.draw.rect(DISPLAYSURF, RED, my_bar_rect)

        enemy_bar_rect = pygame.Rect(WINDOW_WIDTH - enemy_bar_width, enemy_bar_position, enemy_bar_width, enemy_bar_height)
        pygame.draw.rect(DISPLAYSURF, BLUE, enemy_bar_rect)

        # Draw ball
        pygame.draw.circle(DISPLAYSURF, WHITE, (int(ball_position_x), int(ball_position_y)), ball_radius, 0)
        
        # Draw line for seperate game and info
        pygame.draw.line(DISPLAYSURF, WHITE, (WINDOW_WIDTH/2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT), 3)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

# Exit the game
def terminate():
	pygame.quit()
	sys.exit()

# Display score 
def score_msg(score, position):
	scoreSurf = BASIC_FONT.render(str(score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = position
	DISPLAYSURF.blit(scoreSurf, scoreRect)
    	
if __name__ == '__main__':
	main()