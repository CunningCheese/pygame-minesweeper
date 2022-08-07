#A simple python port of minesweeper in pygame
import math
import random
import pygame
from pygame.locals import *

"""
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
"""

block_size = 15


def main(cols, rows):
    pygame.init()

    player_grid = generate_map(8, 8)
    mine_grid = generate_map(8, 8, 8)
    print(mine_grid)


    #logo and title
    logo = pygame.image.load("./resources/mine.jpg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("MINESWEEPER") #title

    screen = pygame.display.set_mode((block_size*cols, block_size*rows)) #display screen

    running = True

    #generate empty board
    for row in range(0, len(mine_grid)):
            for col in range(0, len(mine_grid[row])):
                 draw_tile(row, col, "unclicked", screen)

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
                if (event.button == 1): #check for left click

                    if player_grid[clicked_row][clicked_column] == 0: #check if not clicked
                        player_grid[clicked_row][clicked_column] = 1 #change to clikced

                        if mine_grid[clicked_row][clicked_column]: #check for mines
                            draw_tile(clicked_row, clicked_column, "mine", screen)

                        else:
                            #change to zero tile icon
                            draw_tile(clicked_row, clicked_column, "zero", screen)
                            adjacent = check_adjacent(clicked_column, clicked_row, mine_grid, rows, cols)
                            print(adjacent)

                    else:
                        adjacent = check_adjacent(clicked_column, clicked_row, mine_grid, rows, cols)
                        print(adjacent)

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


#checks for adjacent mines
def check_adjacent(col: int, row: int, mine_map: list, max_rows: int, max_cols: int) -> list:
    
    max_cols -= 1
    max_rows -= 1
    adj_list = []
    
    #check above
    if row > 0 and mine_map[row-1][col] == 1:
        adj_list.append((row-1, col))
        print("Above")
    #check below
    if row < max_rows and mine_map[row+1][col] == 1:
        adj_list.append((row+1, col))
        print("Below")
    #check left
    if col > 0 and mine_map[row][col-1] == 1:
        adj_list.append((row, col-1))
        print("left")
    #check right
    if col < max_cols and mine_map[row][col+1] == 1:
        adj_list.append((row, col+1))
        print("Right")
    
    #check top-left
    if row > 0 and col > 0 and mine_map[row-1][col-1]:
        adj_list.append((row-1, col-1))
        print("Top-left")
    #check top-right
    if row > 0 and col < max_cols and mine_map[row-1][col+1] == 1:
        print("Top-right")
        adj_list.append((row-1, col+1))
    #check bottom-left
    if row < max_rows and col > 0 and mine_map[row+1][col-1]:
        adj_list.append((row+1, col-1))
        print("Bottom left")
    #check bottom-right
    if row < max_rows and col < max_cols and mine_map[row+1][col+1]:
        adj_list.append((row+1, col+1))
        print("Bottom right")

    return adj_list
        

def draw_tile(row, col, tile: str, display):

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

    tile = tile.lower()
    if tile == "unclicked":
        display.blit(unclicked_tile, (col*block_size, row*block_size))
    elif tile == "flag":
        display.blit(flagged_tile, (col*block_size, row*block_size))
    elif tile == "mine":
        display.blit(mine_tile, (col*block_size, row*block_size))
    elif tile == "flagmine":
        display.blit(flagged_mine_tile, (col*block_size, row*block_size))
    elif tile == "zero":
        display.blit(zero_mines, (col*block_size, row*block_size))
    elif tile == "one":
        display.blit(one_mine, (col*block_size, row*block_size))
    elif tile == "two":
        display.blit(two_mines, (col*block_size, row*block_size))
    elif tile == "three":
        display.blit(three_mines, (col*block_size, row*block_size))
    elif tile == "four":
        display.blit(four_mines, (col*block_size, row*block_size))
    elif tile == "five":
        display.blit(five_mines, (col*block_size, row*block_size))
    elif tile == "six":
        display.blit(six_mines, (col*block_size, row*block_size))
    elif tile == "seven":
        display.blit(seven_mines, (col*block_size, row*block_size))
    elif tile == "eight":
        display.blit(eight_mines, (col*block_size, row*block_size))
    else:
        raise RuntimeError("Invalid tile type")
    
    

    pass


if __name__ == "__main__":
    main(8, 8)


