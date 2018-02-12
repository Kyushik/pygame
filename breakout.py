# Q's Vehicle Simulation
# By KyushikMin kyushikmin@gamil.com
# http://mmc.hanyang.ac.kr
# Special thanks to my colleague Hayoung and Jongwon for giving ne the idea of ball and block collision algorithm

import random, sys, time, math, pygame
from pygame.locals import *
import numpy as np
import copy

# Window Information
FPS = 30
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 400

INFO_GAP  = 40
UPPER_GAP = 40
HALF_WINDOW_WIDTH = int(WINDOW_WIDTH / 2)
HALF_WINDOW_HEIGHT = int((WINDOW_HEIGHT - INFO_GAP) / 2)

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

	pygame.display.set_caption('BreakOut')
	# pygame.display.set_icon(pygame.image.load('./Qar_Sim/icon_resize2.png'))

	BASIC_FONT = pygame.font.Font('freesansbold.ttf', 16)

	# Set initial parameters

	init = True
	score = 0
	reward = 0

	bar_width = 60
	bar_height = 8

	bar_init_position = (WINDOW_WIDTH - bar_width)/2
	bar_position = bar_init_position
	bar_speed = 5

	ball_init_position_x = WINDOW_WIDTH / 2
	ball_init_position_y = (WINDOW_HEIGHT - INFO_GAP) / 2 + UPPER_GAP

	ball_position_x = ball_init_position_x
	ball_position_y = ball_init_position_y
	ball_position_x_old = ball_init_position_x
	ball_position_y_old = ball_init_position_y

	ball_radius = 5

	ball_speed_x = random.uniform(-3, 3)
	ball_speed_y = 5
	ball_bounce_speed_range = 10

	block_width  = 48
	block_height = 24

	num_block_row = int(((WINDOW_HEIGHT - INFO_GAP) / 3) / block_height) # Number of rows should be less than 8 or you should add more colors
	num_block_col = int(WINDOW_WIDTH / block_width)

	block_color_list = [RED, LIGHT_ORANGE, YELLOW, GREEN, BLUE, NAVY, PURPLE]

	num_blocks = num_block_row * num_block_col

	init_block_info = []
	for i in range(num_block_row):
		init_block_info.append([])
		for j in range(num_block_col):
			init_block_info[i].append([])

	for i in range(num_block_row):
		for j in range(num_block_col):
			# Horizontal position, Vertical position, Width, Height
			init_block_info[i][j] = [(j * block_width, UPPER_GAP + INFO_GAP + i * block_height, block_width, block_height), 'visible']

	direction = ''
	while True: # Game loop
		# Initial settings
		if init == True:
			bar_position = bar_init_position
			ball_position_x = ball_init_position_x
			ball_position_y = ball_init_position_y

			ball_speed_x = random.uniform(-3, 3)
			ball_speed_y = 5

			block_info = copy.deepcopy(init_block_info)

			init = False

		# Key settings
		for event in pygame.event.get(): # event loop
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a):
					direction = 'LEFT'
				elif (event.key == K_RIGHT or event.key == K_d):
					direction = 'RIGHT'
				elif event.key == K_ESCAPE:
					terminate()
				else:
					direction = 'HOLD'

		# Control the bar
		if direction == 'LEFT':
			bar_position -= bar_speed
		elif direction == 'RIGHT':
			bar_position += bar_speed

		# Constraint of the bar
		if bar_position <= 0:
			bar_position = 0

		if bar_position >= WINDOW_WIDTH - bar_width:
			bar_position = WINDOW_WIDTH - bar_width

		# Move the ball
		ball_position_x += ball_speed_x
		ball_position_y += ball_speed_y

		# Ball is bounced when the ball hit the wall
		if ball_position_x < ball_radius:
			ball_speed_x = - ball_speed_x
			ball_position_x = ball_radius

		if ball_position_x > WINDOW_WIDTH - ball_radius:
			ball_speed_x = - ball_speed_x
			ball_position_x = WINDOW_WIDTH - ball_radius

		if ball_position_y < INFO_GAP + ball_radius:
			ball_speed_y = - ball_speed_y
			ball_position_y = INFO_GAP + ball_radius

		# Ball is bounced when the ball hit the bar
		if ball_position_y > WINDOW_HEIGHT - bar_height - ball_radius:
			# Hit the ball!
			if ball_position_x <= bar_position + bar_width and ball_position_x >= bar_position:
				ball_hit_point = ball_position_x - bar_position
				ball_hit_point_ratio = ball_hit_point / bar_width

				ball_speed_x = (ball_hit_point_ratio * ball_bounce_speed_range) - (ball_bounce_speed_range/2)

				# if abs(ball_hit_point_ratio - 0.5) < 0.01:
				# 	ball_speed_x = random.uniform(-0.01 * ball_bounce_speed_range/2 , 0.01 * ball_bounce_speed_range/2)

				# ball_speed_x = (ball_hit_point_ratio * ball_bounce_speed_range) - (ball_bounce_speed_range/2)
				ball_speed_y = - ball_speed_y
				ball_position_y = WINDOW_HEIGHT - bar_height - ball_radius

			# Lose :(
		if ball_position_y >= WINDOW_HEIGHT:
			init = True

		# When the ball hit the block
		check_ball_hit_block = 0
		for i in range(num_block_row):
			for j in range(num_block_col):
				block_left  = block_info[i][j][0][0]
				block_right = block_info[i][j][0][0] + block_info[i][j][0][2]
				block_up    = block_info[i][j][0][1]
				block_down  = block_info[i][j][0][1] + block_info[i][j][0][3]
				visible     = block_info[i][j][1]

				# The ball hit some block!!
				# if (block_left <= ball_position_x + ball_radius) and (ball_position_x - ball_radius <= block_right) and (block_up <= ball_position_y + ball_radius) and (ball_position_y - ball_radius <= block_down) and visible == 'visible':
				if (block_left <= ball_position_x) and (ball_position_x <= block_right) and (block_up <= ball_position_y) and (ball_position_y <= block_down) and visible == 'visible':
					# Which part of the block was hit??
					# Upper left, Upper right, Lower right, Lower left
					block_points = [[block_left, block_up], [block_right, block_up], [block_right, block_down], [block_left, block_down]]

					if ball_position_x - ball_position_x_old == 0:
						slope_ball = (ball_position_y - ball_position_y_old) / (0.01)
					else:
						slope_ball = (ball_position_y - ball_position_y_old) / (ball_position_x - ball_position_x_old)

					# ax+by+c = 0
					line_coeff = [slope_ball, -1, ball_position_y_old - (slope_ball * ball_position_x_old)]

					point1 = [block_left, (-1/line_coeff[1]) * (line_coeff[0] * block_left + line_coeff[2])]
					point2 = [block_right, (-1/line_coeff[1]) * (line_coeff[0] * block_right + line_coeff[2])]
					point3 = [(-1/line_coeff[0]) * (line_coeff[1] * block_up + line_coeff[2]), block_up]
					point4 = [(-1/line_coeff[0]) * (line_coeff[1] * block_down + line_coeff[2]), block_down]

					# Left, Right, Up, Down
					intersection = [point1, point2, point3, point4]
					check_intersection = [0, 0, 0, 0]

					for k in range(len(intersection)):
						#intersection point is on the left side of block
						if (intersection[k][0] == block_left) and (block_up <= intersection[k][1] <= block_down):
							check_intersection[0] = 1

						if (intersection[k][0] == block_right) and (block_up <= intersection[k][1] <= block_down):
							check_intersection[1] = 1

						if (intersection[k][1] == block_up) and (block_left <= intersection[k][0] <= block_right):
							check_intersection[2] = 1

						if (intersection[k][1] == block_down) and (block_left <= intersection[k][0] <= block_right):
							check_intersection[3] = 1

					dist_points = [np.inf, np.inf, np.inf, np.inf]
					for k in range(len(intersection)):
						if check_intersection[k] == 1:
							dist = get_dist(intersection[k], [ball_position_x_old, ball_position_y_old])
							dist_points[k] = dist

					# 0: Left, 1: Right, 2: Up, 3: Down
					collision_line = np.argmin(dist_points)

					if collision_line == 0:
						ball_speed_x = - ball_speed_x
					elif collision_line == 1:
						ball_speed_x = - ball_speed_x
					elif collision_line == 2:
						ball_speed_y = - ball_speed_y
					elif collision_line == 3:
						ball_speed_y = - ball_speed_y

					# Incorrect breaking at corner!
					# e.g. block was hit on the right side even though there is visible block on the right
					# Then, the former decision was wrong, so change the direction!
					if j > 0:
						if collision_line == 0 and block_info[i][j-1][1] == 'visible':
							ball_speed_x = - ball_speed_x
							ball_speed_y = - ball_speed_y
					if j < num_block_col - 1:
						if collision_line == 1 and block_info[i][j+1][1] == 'visible':
							ball_speed_x = - ball_speed_x
							ball_speed_y = - ball_speed_y
					if i > 0:
						if collision_line == 2 and block_info[i-1][j][1] == 'visible':
							ball_speed_x = - ball_speed_x
							ball_speed_y = - ball_speed_y
					if i < num_block_row - 1:
						if collision_line == 3 and block_info[i+1][j][1] == 'visible':
							ball_speed_x = - ball_speed_x
							ball_speed_y = - ball_speed_y

					# Move the ball to the block boundary after ball hit the block
					if collision_line == 0:
						ball_position_x = block_left - ball_radius
					elif collision_line == 1:
						ball_position_x = block_right + ball_radius
					elif collision_line == 2:
						ball_position_y = block_up - ball_radius
					elif collision_line == 3:
						ball_position_y = block_down + ball_radius

					# make hit block invisible
					block_info[i][j][1] = 'invisible'
					check_ball_hit_block = 1

				# If one block is hitted, break the for loop (Preventing to break multiple blocks at once)
				if check_ball_hit_block == 1:
					break
			# If one block is hitted, break the for loop (Preventing to break multiple blocks at once)
			if check_ball_hit_block == 1:
				break

		# Fill background color
		DISPLAYSURF.fill(BLACK)

		# Draw blocks
		count_visible = 0
		for i in range(num_block_row):
			for j in range(num_block_col):
				if block_info[i][j][1] == 'visible':
					pygame.draw.rect(DISPLAYSURF, block_color_list[i], block_info[i][j][0])
					count_visible += 1

		# Win the game!! :)
		if count_visible == 0:
			init = True

		# Display informations
		score_msg(num_blocks - count_visible)
		block_num_msg(count_visible)

		# Draw bar
		bar_rect = pygame.Rect(bar_position, WINDOW_HEIGHT - bar_height, bar_width, bar_height)
		pygame.draw.rect(DISPLAYSURF, RED, bar_rect)

		ball_position_x_old = ball_position_x
		ball_position_y_old = ball_position_y

		# Draw ball
		pygame.draw.circle(DISPLAYSURF, WHITE, (int(ball_position_x), int(ball_position_y)), ball_radius, 0)

		# Draw line for seperate game and info
		pygame.draw.line(DISPLAYSURF, WHITE, (0, 40), (WINDOW_WIDTH, 40), 3)

		pygame.display.update()
		FPS_CLOCK.tick(FPS)

# Exit the game
def terminate():
	pygame.quit()
	sys.exit()

# Display score
def score_msg(score):
	scoreSurf = BASIC_FONT.render('Score: ' + str(score), True, WHITE)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (10, 10)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

# Display how many blocks are left
def block_num_msg(num_blocks):
	blockNumSurf = BASIC_FONT.render('Number of Blocks: ' + str(num_blocks), True, WHITE)
	blockNumRect = blockNumSurf.get_rect()
	blockNumRect.topleft = (WINDOW_WIDTH - 180, 10)
	DISPLAYSURF.blit(blockNumSurf, blockNumRect)

def dist_line_point(coeff, point):
	dist = abs(coeff[0] * point[0] + coeff[1] * point[1] +coeff[2]) / math.sqrt(math.pow(coeff[0],2) + math.pow(coeff[1],2))
	return dist

def get_dist(point1, point2):
	return math.sqrt(math.pow(point1[0] - point2[0],2) + math.pow(point1[1] - point2[1], 2))

if __name__ == '__main__':
	main()
