#A simple python port of minesweeper in pygame
import math
import random
import pygame
from pygame.locals import *

mine_grid = [ #mine = 1, no_mine = 0
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

    player_grid = generate_map(8, 8)
    mine_map = generate_map(8, 8, 8)
    print(mine_map)

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
            
            if event.type == pygame.MOUSEBUTTONUP: # if clicked
                mousePos = pygame.mouse.get_pos()
                clicked_tile = parse_click(mousePos[0], mousePos[1])
                clicked_row = clicked_tile[0]
                clicked_column = clicked_tile[1]

                print(clicked_tile)

                if player_grid[clicked_row][clicked_column] == 0: #check if not clicked
                    player_grid[clicked_row][clicked_column] = 1 #change to clicked
                    screen.blit(zero_mines, (clicked_column*block_size, clicked_row*block_size)) #palceholder
                else:
                    print("clicked!")

        pygame.display.update()



def parse_click(x, y): #returns row and colum clicked based on x and y coords
    row = math.floor(y/block_size)
    col = math.floor(x/block_size)

    return (row, col)


#generates empty 2d list if no mines specified
#if mines specified
def generate_map(cols: int, rows: int, mine_count: int = None) -> list: 
    if mine_count == None: #generate empty map
        map = [[0 for _ in range(cols)] for _ in range(rows)]

    else: #generate map with mines
        total_tiles = cols*rows

        if mine_count >= total_tiles:
            raise ValueError("More mines than tiles!")
        
        # generate random positions for mines          
        mine_list = random.sample(range(1, total_tiles+1), mine_count)

        map = generate_map(cols, rows) #empty map
        print(map) 
        pos = 0
        
        #place mines on map
        cur_row = 0
        for row in map:
            cur_col = 0
            for col in row:
                pos += 1
                if pos in mine_list:
                    map[cur_row][cur_col] = 1
                cur_col += 1
            cur_row += 1
            
        

    return list(map)



if __name__ == "__main__":
    main(8, 8)


