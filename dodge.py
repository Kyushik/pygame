# Dodge

# Rule
'''
Blue ball is agent and red ball is enemy.
If agent collide with enemy, game is over
Evade the enemy as long as possible!!
'''

# By KyushikMin kyushikmin@gamil.com
# http://mmc.hanyang.ac.kr

import random, sys, time, math, pygame
from pygame.locals import *
import numpy as np
import copy

# Window Information
FPS = 30

GAP_WIDTH = 10
TOP_WIDTH = 40

WINDOW_WIDTH = 360
WINDOW_HEIGHT = WINDOW_WIDTH + TOP_WIDTH

HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int(WINDOW_HEIGHT / 2)

CENTER_X = int(WINDOW_WIDTH / 2)
CENTER_Y = int(TOP_WIDTH + (WINDOW_HEIGHT - TOP_WIDTH)/2)

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

    pygame.display.set_caption('Dodge')

    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 16)

    # Set initial parameters

    init = True
    my_time = 0
    start_time = time.time()

    my_radius = 10
    my_init_position = [CENTER_X - int(my_radius/2), CENTER_Y - int(my_radius/2)]
    my_position = my_init_position
    my_speed = 5

    num_balls = 10
    gap_balls = 20

    # Set ball position and velocity
    # Ball_list: ID, x_position, y_position, x_velocity, y_velocity
    min_ball_speed = 3.0
    max_ball_speed = 6.0

    ball_list = set_ball_pos_and_vel(num_balls, gap_balls, min_ball_speed, max_ball_speed)
    ball_radius = 4

    direction = ''
    while True: # Game loop
        # Initial settings
        if init == True:
            my_position = [CENTER_X - int(my_radius/2), CENTER_Y - int(my_radius/2)]
            ball_list = set_ball_pos_and_vel(num_balls, gap_balls, min_ball_speed, max_ball_speed)

            start_time = time.time()

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
                elif (event.key == K_LEFT):
                    direction = 'LEFT'
                elif (event.key == K_RIGHT):
                    direction = 'RIGHT'
                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    init = True
                else:
                    direction = 'HOLD'

        # Control the bar
        if direction == 'UP':
            my_position[1] -= my_speed
        elif direction == 'DOWN':
            my_position[1] += my_speed
        elif direction == 'LEFT':
            my_position[0] -= my_speed
        elif direction == 'RIGHT':
            my_position[0] += my_speed

        # Constraint of the agent
        my_position = constraint(my_position, my_radius)

        # Update ball
        ball_list = update_balls(ball_list, ball_radius)

        # Lose :(
        init = check_lose(my_position, my_radius, ball_list, ball_radius, start_time)

        # Fill background color
        DISPLAYSURF.fill(BLACK)

        # Display time
        time_msg("Survival Time: " + str(time.time() - start_time), (10, 15))

        # Draw agent
        pygame.draw.circle(DISPLAYSURF, BLUE, (int(my_position[0]), int(my_position[1])), my_radius, 0)

        # Draw ball
        for i in range(len(ball_list)):
            pygame.draw.circle(DISPLAYSURF, RED, (int(ball_list[i][1]), int(ball_list[i][2])), ball_radius, 0)

        # Draw lines for gameboard
        draw_board()

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

# Exit the game
def terminate():
	pygame.quit()
	sys.exit()

# Set random position and velocity
def set_ball_pos_and_vel(num_balls, gap_balls, min_ball_speed, max_ball_speed):
    rand_pos_x = 0
    rand_pos_y = 0
    rand_vel_x = 0
    rand_vel_y = 0

    ball_list = []

    for i in range(num_balls):
        ball_list.append([])

        # Get random numbers
        rand_pos_x = random.random()
        rand_pos_y = random.random()
        rand_vel_x = random.random()
        rand_vel_y = random.random()

        ball_list[i].append(i) # id

        # initial x position
        if rand_pos_x > 0.5:
            ball_list[i].append(random.randint(CENTER_X + gap_balls, WINDOW_WIDTH - gap_balls))
        else:
            ball_list[i].append(random.randint(gap_balls, CENTER_X - gap_balls))

        # initial y position
        if rand_pos_y > 0.5:
            ball_list[i].append(random.randint(CENTER_Y + gap_balls, WINDOW_HEIGHT - gap_balls))
        else:
            ball_list[i].append(random.randint(TOP_WIDTH + gap_balls, CENTER_Y - gap_balls))

        # initial x velocity
        if rand_vel_x > 0.5:
            ball_list[i].append(random.uniform(min_ball_speed, max_ball_speed))
        else:
            ball_list[i].append(-random.uniform(min_ball_speed, max_ball_speed))

        # initial y velocity
        if rand_vel_y > 0.5:
            ball_list[i].append(random.uniform(min_ball_speed, max_ball_speed))
        else:
            ball_list[i].append(-random.uniform(min_ball_speed, max_ball_speed))

    return ball_list

# Keep the agent inside gameboard
def constraint(my_position, my_radius):
    if my_position[0] <= GAP_WIDTH + my_radius:
        my_position[0] = GAP_WIDTH + my_radius

    if my_position[0] >= WINDOW_WIDTH - GAP_WIDTH - my_radius:
        my_position[0] = WINDOW_WIDTH - GAP_WIDTH - my_radius

    if my_position[1] >= WINDOW_HEIGHT - GAP_WIDTH - my_radius:
        my_position[1] = WINDOW_HEIGHT - GAP_WIDTH - my_radius

    if my_position[1] <= TOP_WIDTH + GAP_WIDTH + my_radius:
        my_position[1] = TOP_WIDTH + GAP_WIDTH + my_radius

    return my_position

# Update balls
def update_balls(ball_list, ball_radius):
    for i in range(len(ball_list)):
        # Move the balls
        ball_list[i][1] += ball_list[i][3]
        ball_list[i][2] += ball_list[i][4]

        # If ball hits the ball, it bounce
        if ball_list[i][1] <= GAP_WIDTH + ball_radius:
            ball_list[i][1] = GAP_WIDTH + ball_radius + 1
            ball_list[i][3] = -ball_list[i][3]

        if ball_list[i][1] >= WINDOW_WIDTH - GAP_WIDTH - ball_radius:
            ball_list[i][1] = WINDOW_WIDTH - GAP_WIDTH - ball_radius - 1
            ball_list[i][3] = -ball_list[i][3]

        if ball_list[i][2] >= WINDOW_HEIGHT - GAP_WIDTH - ball_radius:
            ball_list[i][2] = WINDOW_HEIGHT - GAP_WIDTH - ball_radius - 1
            ball_list[i][4] = -ball_list[i][4]

        if ball_list[i][2] <= TOP_WIDTH + GAP_WIDTH + ball_radius:
            ball_list[i][2] = TOP_WIDTH + GAP_WIDTH + ball_radius + 1
            ball_list[i][4] = -ball_list[i][4]

    return ball_list

# Check lose
def check_lose(my_position, my_radius, ball_list, ball_radius, start_time):
    # check collision
    for i in range(10):
        x_square = (my_position[0] - ball_list[i][1]) ** 2
        y_square = (my_position[1] - ball_list[i][2]) ** 2
        dist_balls = my_radius + ball_radius

        if (np.sqrt(x_square + y_square) < dist_balls):
            print("Survival time: " + str(time.time() - start_time))
            return True

    return False

# Display time
def time_msg(survive_time, position):
	timeSurf = BASIC_FONT.render(str(survive_time), True, WHITE)
	timeRect = timeSurf.get_rect()
	timeRect.topleft = position
	DISPLAYSURF.blit(timeSurf, timeRect)

# Draw gameboard
def draw_board():
    pygame.draw.line(DISPLAYSURF, WHITE, (GAP_WIDTH, TOP_WIDTH + GAP_WIDTH), (GAP_WIDTH, WINDOW_HEIGHT - GAP_WIDTH), 3)
    pygame.draw.line(DISPLAYSURF, WHITE, (WINDOW_WIDTH - GAP_WIDTH, TOP_WIDTH + GAP_WIDTH), (WINDOW_WIDTH - GAP_WIDTH, WINDOW_HEIGHT - GAP_WIDTH), 3)
    pygame.draw.line(DISPLAYSURF, WHITE, (GAP_WIDTH, TOP_WIDTH + GAP_WIDTH), (WINDOW_WIDTH - GAP_WIDTH, TOP_WIDTH + GAP_WIDTH), 3)
    pygame.draw.line(DISPLAYSURF, WHITE, (GAP_WIDTH, WINDOW_HEIGHT - GAP_WIDTH), (WINDOW_WIDTH - GAP_WIDTH, WINDOW_HEIGHT - GAP_WIDTH), 3)

if __name__ == '__main__':
	main()
