#A simple python port of minesweeper in pygame
import math
import pygame
from pygame.locals import *

mine_grid = [ #mine = 1, nomine = 0
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]

player_grid = [ #clicked = 1, unclicked = 0
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]

block_size = 15


def main(cols, rows):
    pygame.init()

    # IMAGES INIT
    unclicked_tile = pygame.image.load("./resources/unclicked.jpg")
    flagged_tile = pygame.image.load("./resources/flag.jpg")
    mine_tile = pygame.image.load("./resources/mine.jpg")
    flagged_mine_tile = pygame.image.load("./resources/mineflag.jpg")

    zero_mines = pygame.image.load("./resources/0.jpg")
    one_mine = pygame.image.load("./resources/1.jpg")
    two_mines = pygame.image.load("./resources/2.jpg")
    three_mines = pygame.image.load("./resources/3.jpg")
    four_mines = pygame.image.load("./resources/4.jpg")
    five_mines = pygame.image.load("./resources/5.jpg")
    six_mines = pygame.image.load("./resources/6.jpg")
    seven_mines = pygame.image.load("./resources/7.jpg")
    eight_mines = pygame.image.load("./resources/8.jpg")


    #logo and title
    logo = mine_tile
    pygame.display.set_icon(logo)
    pygame.display.set_caption("MINESWEEPER") #title

    screen = pygame.display.set_mode((block_size*cols, block_size*rows)) #display screen

    running = True

    #generate empty board
    for row in range(0, len(mine_grid)):
            for col in range(0, len(mine_grid[row])):
                 screen.blit(unclicked_tile, (col*block_size, row*block_size))

    while running: #main loop
        
        #write tiles from map
        

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
            
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                clicked_tile = parse_click(mousePos[0], mousePos[1])
                clicked_row = clicked_tile[0]
                clicked_column = clicked_tile[1]

                print(clicked_tile)

                if player_grid[clicked_row][clicked_column] == 0: #check if clicked
                    player_grid[clicked_row][clicked_column] = 1 #change to clicked
                    screen.blit(zero_mines, (clicked_column*block_size, clicked_row*block_size)) #

        pygame.display.update()



def parse_click(x, y): #returns row and colum clicked based on x and y coords
    row = math.floor(y/block_size)
    col = math.floor(x/block_size)

    return (row, col)



def generate_map(cols, rows):
    pass



if __name__ == "__main__":
    main(8, 8)


