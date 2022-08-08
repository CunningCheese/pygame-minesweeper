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


def main(cols, rows, mine_num):
    pygame.init()

    assert mine_num < rows*cols, "Invalid Mine Count"

    global player_grid, mine_grid, screen

    player_grid = generate_map(cols, rows)
    mine_grid = generate_map(cols, rows, mine_num)
    # print(mine_grid)


    #logo and title
    logo = pygame.image.load("./resources/mine.jpg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("MINESWEEPER") #title

    screen = pygame.display.set_mode((block_size*cols, block_size*rows)) #display screen

    running = True

    #generate empty board
    for row in range(0, len(mine_grid)):
            for col in range(0, len(mine_grid[row])):
                 draw_tile(row, col, "unclicked")

    while running: #main loop        

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
            
            if event.type == pygame.MOUSEBUTTONUP: # if clicked
                mousePos = pygame.mouse.get_pos()
                clicked_tile = parse_click(mousePos[0], mousePos[1])
                clicked_row = clicked_tile[0]
                clicked_column = clicked_tile[1]

                # print(clicked_tile)
                if (event.button == 1): #check for left click

                    if player_grid[clicked_row][clicked_column] == 0: #check if not revealed
                        player_grid[clicked_row][clicked_column] = 1 #change to revealed

                        if mine_grid[clicked_row][clicked_column]: #check if mine clicked
                            draw_tile(clicked_row, clicked_column, "mine")

                        else:
                            #find adjacent tiles
                            adjacent_tiles = find_adjacent(clicked_column, clicked_row)
                            print(adjacent_tiles)
                            adj_mines = adjacent_tiles[0]
                            mine_count = len(adj_mines)
                            adj_empty = adjacent_tiles[1]

                            #render numbered block
                            if mine_count == 0:
                                draw_tile(clicked_row, clicked_column, "zero")
                                render_adjacent(adjacent_tiles)
                            elif mine_count == 1:
                                draw_tile(clicked_row, clicked_column, "one")
                            elif mine_count == 2:
                                draw_tile(clicked_row, clicked_column, "two")
                            elif mine_count == 3:
                                draw_tile(clicked_row, clicked_column, "three")
                            elif mine_count == 4:
                                draw_tile(clicked_row, clicked_column, "four")
                            elif mine_count == 5:
                                draw_tile(clicked_row, clicked_column, "five")
                            elif mine_count == 6:
                                draw_tile(clicked_row, clicked_column, "six")
                            elif mine_count == 7:
                                draw_tile(clicked_row, clicked_column, "seven")
                            elif mine_count == 8:
                                draw_tile(clicked_row, clicked_column, "eight")

                            
                            



                    else:
                        adjacent_tiles = find_adjacent(clicked_column, clicked_row)
                        # print(adjacent_tiles)
                        pass
            


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


#checks for adjacent mines and empty tiles
#returns list = [[mine-coords], [empty-coords]]
#(can't go out of bounds)
def find_adjacent(row, col):
    max_rows = len(mine_grid[0])-1
    max_cols = len(mine_grid)-1

    final_adj = []
    empty_adj = []
    mine_adj = []

    for col_diff in (-1, 0, 1):
        for row_diff in (-1, 0, 1):
            if col_diff == 0 and row_diff == 0:
                continue
            new_col, new_row = col + col_diff, row + row_diff
            if new_col < 0 or new_col > max_cols:
                continue
            if new_row < 0 or new_row > max_rows:
                continue

            if mine_grid[new_col][new_row] == 1:
                mine_adj.append((new_col, new_row))
            else:
                empty_adj.append((new_col, new_row))

    final_adj = [mine_adj, empty_adj]
    return final_adj


def render_adjacent(full_adj: list): # displays the tiles around a 'zero' tile, use mine list
    max_rows = len(mine_grid)-1
    max_col = len(mine_grid[0])-1

    for tile in full_adj[1]: #loop through adjacent tiles
        if (tile[0] <= max_rows and tile[0] >= 0) and (tile[1] <= max_col): # check if in bounds
            tile_adj = find_adjacent(tile[1], tile[0])
            mine_count = len(tile_adj[0])
            row = tile[0]
            col = tile[1]

            if player_grid[row][col] == 0: #check if not revealed
                player_grid[row][col] = 1 #change to revealed
                if mine_count == 0:
                    draw_tile(row, col, "zero")
                    render_adjacent(tile_adj)  
                elif mine_count == 1:
                    draw_tile(row, col, "one")
                elif mine_count == 2:
                    draw_tile(row, col, "two")
                elif mine_count == 3:
                    draw_tile(row, col, "three")
                elif mine_count == 4:
                    draw_tile(row, col, "four")
                elif mine_count == 5:
                    draw_tile(row, col, "five")
                elif mine_count == 6:
                    draw_tile(row, col, "six")
                elif mine_count == 7:
                    draw_tile(row, col, "seven")
                elif mine_count == 8:
                    draw_tile(row, col, "eight")  
        

def draw_tile(row: int, col: int, tile: str) -> None:

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
        screen.blit(unclicked_tile, (col*block_size, row*block_size))
    elif tile == "flag":
        screen.blit(flagged_tile, (col*block_size, row*block_size))
    elif tile == "mine":
        screen.blit(mine_tile, (col*block_size, row*block_size))
    elif tile == "flagmine":
        screen.blit(flagged_mine_tile, (col*block_size, row*block_size))
    elif tile == "zero":
        screen.blit(zero_mines, (col*block_size, row*block_size))
    elif tile == "one":
        screen.blit(one_mine, (col*block_size, row*block_size))
    elif tile == "two":
        screen.blit(two_mines, (col*block_size, row*block_size))
    elif tile == "three":
        screen.blit(three_mines, (col*block_size, row*block_size))
    elif tile == "four":
        screen.blit(four_mines, (col*block_size, row*block_size))
    elif tile == "five":
        screen.blit(five_mines, (col*block_size, row*block_size))
    elif tile == "six":
        screen.blit(six_mines, (col*block_size, row*block_size))
    elif tile == "seven":
        screen.blit(seven_mines, (col*block_size, row*block_size))
    elif tile == "eight":
        screen.blit(eight_mines, (col*block_size, row*block_size))
    else:
        raise RuntimeError("Invalid tile type")


if __name__ == "__main__":
    main(8, 8, 8)


