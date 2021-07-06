import pygame
import sys
import numpy as np
import copy
import math
import time

try:
    NUM_BLOCKS = int(input("Amount of blocks^2: "))
    gen_time = float(input("Delay between genereations in seconds (float): "))
except:
    print("Not valid input")

blockSize = 20

pygame.init()
pygame.display.set_caption('Game of Life by Vegard Hansen Stenberg')
SCREEN = pygame.display.set_mode((NUM_BLOCKS*blockSize, NUM_BLOCKS*blockSize))
SCREEN.fill((0,0,0))

game_running = False

current_cells = np.zeros((NUM_BLOCKS, NUM_BLOCKS))
next_gen = np.zeros((NUM_BLOCKS, NUM_BLOCKS))

def check_live_neighbours(x, y):
    neighbours = 0

    if x != 0 and y != 0 and current_cells[y-1, x-1]:
        neighbours += 1
    if x != 0 and current_cells[y, x-1]:
        neighbours += 1
    if x != 0 and y != NUM_BLOCKS-1 and current_cells[y+1, x-1]:
        neighbours += 1
    if y != 0 and x != NUM_BLOCKS-1 and current_cells[y-1, x+1]:
        neighbours += 1
    if x != NUM_BLOCKS-1 and current_cells[y, x+1]:
        neighbours += 1
    if x != NUM_BLOCKS-1 and y != NUM_BLOCKS-1  and current_cells[y+1, x+1]:
        neighbours += 1
    if y != 0 and current_cells[y-1, x]:
        neighbours += 1
    if y != NUM_BLOCKS-1 and current_cells[y+1, x]:
        neighbours += 1

    return neighbours

while True:
    for x in range(0, NUM_BLOCKS*blockSize, blockSize):
        for y in range(0, NUM_BLOCKS*blockSize, blockSize):
            cell_x = int(x/20)
            cell_y = int(y/20)

            if current_cells[cell_y, cell_x] == 0:
                # Draw current cells
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(SCREEN, (0, 0, 0), rect, 0)

                # Calculate next gen
                if game_running:
                    neighbours = check_live_neighbours(cell_x, cell_y)

                    if neighbours == 3:
                        next_gen[cell_y, cell_x] = 1
                    else:
                        next_gen[cell_y, cell_x] = 0

            elif current_cells[cell_y, cell_x] == 1:
                # Draw current cells
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(SCREEN, (255, 255, 255), rect, 0)

                # Calculate next gen
                if game_running:
                    neighbours = check_live_neighbours(cell_x, cell_y)

                    if neighbours == 2 or neighbours == 3:
                        next_gen[cell_y, cell_x] = 1
                    else:
                        next_gen[cell_y, cell_x] = 0

    if game_running:
        current_cells = np.copy(next_gen)
        time.sleep(gen_time)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_running:
                x, y = event.pos
                x, y = math.floor(x / 20), math.floor(y / 20)

                current_cells[y, x] = 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_running = True

        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
