#A simple python port of minesweeper in pygame
import math
import random
import time
import pygame
from pygame.locals import *

"""
player_grid = [ #clicked = 1, unclicked = 0 #flaged = 2
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
scale = 2


    # IMAGES INIT
unclicked_tile = pygame.transform.scale(pygame.image.load("./resources/unclicked.jpg"), (block_size*scale, block_size*scale))
flagged_tile = pygame.transform.scale(pygame.image.load("./resources/flag.jpg"), (block_size*scale, block_size*scale))
mine_tile = pygame.transform.scale(pygame.image.load("./resources/mine.jpg"), (block_size*scale, block_size*scale))
flagged_mine_tile = pygame.transform.scale(pygame.image.load("./resources/mineflag.jpg"), (block_size*scale, block_size*scale))

zero_mines = pygame.transform.scale(pygame.image.load("./resources/0.jpg"), (block_size*scale, block_size*scale))
one_mine = pygame.transform.scale(pygame.image.load("./resources/1.jpg"), (block_size*scale, block_size*scale))
two_mines = pygame.transform.scale(pygame.image.load("./resources/2.jpg"), (block_size*scale, block_size*scale))
three_mines = pygame.transform.scale(pygame.image.load("./resources/3.jpg"), (block_size*scale, block_size*scale))
four_mines = pygame.transform.scale(pygame.image.load("./resources/4.jpg"), (block_size*scale, block_size*scale))
five_mines = pygame.transform.scale(pygame.image.load("./resources/5.jpg"), (block_size*scale, block_size*scale))
six_mines = pygame.transform.scale(pygame.image.load("./resources/6.jpg"), (block_size*scale, block_size*scale))
seven_mines = pygame.transform.scale(pygame.image.load("./resources/7.jpg"), (block_size*scale, block_size*scale))
eight_mines = pygame.transform.scale(pygame.image.load("./resources/8.jpg"), (block_size*scale, block_size*scale))

def main(cols: int, rows: int, mine_num: int):
    pygame.init()

    assert mine_num < rows*cols, "Invalid Mine Count"

    global player_grid, mine_grid, screen

    player_grid = generate_map(cols, rows)


    #logo and title
    logo = pygame.image.load("./resources/mine.jpg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("MINESWEEPER") #title

    screen = pygame.display.set_mode((block_size*cols*scale, block_size*rows*scale)) #display screen

    clock = pygame.time.Clock() # for FPS

    running = True
    quit = False
    lost = False
    has_clicked_once = False

    #generate empty board
    for row in range(0, len(player_grid)):
            for col in range(0, len(player_grid[row])):
                 draw_tile(row, col, "unclicked")

    while running: #main loop        

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
                quit = True
            
            if event.type == pygame.MOUSEBUTTONUP: # if clicked
                mousePos = pygame.mouse.get_pos()
                clicked_tile = parse_click(mousePos[0], mousePos[1])
                clicked_row = clicked_tile[0]
                clicked_column = clicked_tile[1]

                if (event.button == 1): # check for left click

                    if has_clicked_once == False:
                        has_clicked_once = True
                        mine_grid = generate_map(cols, rows, mine_num, (clicked_row, clicked_column))

                        
                    if player_grid[clicked_row][clicked_column] == 0: #check if not revealed or flagged
                        player_grid[clicked_row][clicked_column] = 1 #change to revealed

                        if mine_grid[clicked_row][clicked_column] == 1: #check if mine clicked
                            render_all_mines()
                            running = False
                            lost = True


                        else:
                            #find adjacent tiles
                            adjacent_tiles = find_adjacent(clicked_column, clicked_row)
                            adj_mines = adjacent_tiles[0]
                            adj_mine_count = len(adj_mines)
                            adj_empty = adjacent_tiles[1]

                            #render numbered block
                            if adj_mine_count == 0:
                                draw_tile(clicked_row, clicked_column, "zero")
                                render_adjacent(adjacent_tiles)
                            elif adj_mine_count == 1:
                                draw_tile(clicked_row, clicked_column, "one")
                            elif adj_mine_count == 2:
                                draw_tile(clicked_row, clicked_column, "two")
                            elif adj_mine_count == 3:
                                draw_tile(clicked_row, clicked_column, "three")
                            elif adj_mine_count == 4:
                                draw_tile(clicked_row, clicked_column, "four")
                            elif adj_mine_count == 5:
                                draw_tile(clicked_row, clicked_column, "five")
                            elif adj_mine_count == 6:
                                draw_tile(clicked_row, clicked_column, "six")
                            elif adj_mine_count == 7:
                                draw_tile(clicked_row, clicked_column, "seven")
                            elif adj_mine_count == 8:
                                draw_tile(clicked_row, clicked_column, "eight")

                    else: #if revealed...
                        pass
                if (event.button == 3 and has_clicked_once == True): #right click
                    if player_grid[clicked_row][clicked_column] == 2: # check if flagged
                        player_grid[clicked_row][clicked_column] = 0 # change to not flagged
                        draw_tile(clicked_row, clicked_column, "unclicked") # update to unclicked
                    elif player_grid[clicked_row][clicked_column] == 0: # if not flagged and not revealed
                        player_grid[clicked_row][clicked_column] = 2 # change to flagged
                        draw_tile(clicked_row, clicked_column, "flag") # update to flagged
                    pass
                
                print(player_grid)
        
        # win condition
        if has_clicked_once:
            if check_win(mine_num):
                print("WINNER???? I HARDLY EVEN KNOW HER!!!!!!!")
                running = False

    
        pygame.display.update()
        clock.tick(30) # framerate 

    if quit == False:
        time.sleep(2)
        # if lost:
        #     lose_animation()
        # else:
        #     win_animation()
        time.sleep(1)
        main(cols, rows, mine_num)


def parse_click(x, y): #returns row and colum clicked based on x and y coords
    row = math.floor(y/block_size/scale)
    col = math.floor(x/block_size/scale)

    return (row, col)


#generates empty 2d list if no mines specified
#if mines specified
def generate_map(cols: int, rows: int, mine_count: int = None, start_click: tuple = None) -> list: 
    if mine_count == None: #generate empty map
        map = [[0 for _ in range(cols)] for _ in range(rows)]

    else: #generate map with mines
        total_tiles = cols*rows
        
        start_click_int = 0
        fin_clk = 0
        for row in range(0, rows):
            for col in range(0, cols):
                start_click_int += 1
                if (row, col) == start_click:
                    fin_clk = start_click_int
                

        first_run = True
        # generate random positions for mines         
        while first_run or (fin_clk in mine_list):
            mine_list = random.sample(range(1, total_tiles+1), mine_count)
            first_run = False


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


def win_animation():
    for row in range(len(player_grid)):
        for col in range(len(player_grid[0])):
            draw_tile(row, col, "green")
            time.sleep(0.2)
            pygame.display.update()

def lose_animation():
    for row in range(len(player_grid)):
        for col in range(len(player_grid[0])):
            draw_tile(row, col, "red")
            time.sleep(0.1)
            pygame.display.update()


def check_win(mine_count):
    not_mine_count = (len(player_grid) * len(player_grid[0])) - mine_count
    
    total_revealed = 0
    for row in player_grid:
        for col in row:
            if col == 1:
                total_revealed += 1

    if total_revealed == not_mine_count:
        return True
    return False          


def render_adjacent(full_adj: list): # displays the tiles around a 'zero' tile, use mine list
    max_rows = len(mine_grid)-1
    max_col = len(mine_grid[0])-1

    for tile in full_adj[1]: #loop through adjacent tiles
        if (tile[0] <= max_rows and tile[0] >= 0) and (tile[1] <= max_col and tile[1] >= 0): # check if in bounds
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

def render_all_mines(): # render all mines on screen on lose
    cur_row = 0
    for row in mine_grid:
        cur_col = 0
        for col in row:
            if col == 1: # mine detected
                player_grid[cur_row][cur_col] = 1
                draw_tile(cur_row, cur_col, "mine")
            cur_col += 1
        cur_row += 1
    
    for row in range(0, len(player_grid)): #check if incorrect flag placement
        for col in range(0, len(player_grid[0])):
            if player_grid[row][col] == 2:
                if mine_grid[row][col] != 1:
                    draw_tile(row, col, "flagmine")



        

def draw_tile(row: int, col: int, tile: str) -> None:

    tile = tile.lower()

    if tile == "unclicked":
        screen.blit(unclicked_tile, (col*block_size*scale, row*block_size*scale))
    elif tile == "flag":
        screen.blit(flagged_tile, (col*block_size*scale, row*block_size*scale))
    elif tile == "mine":
        screen.blit(mine_tile, (col*block_size*scale, row*block_size*scale))
    elif tile == "flagmine":
        screen.blit(flagged_mine_tile, (col*block_size*scale, row*block_size*scale))

    elif tile == "zero":
        screen.blit(zero_mines, (col*block_size*scale, row*block_size*scale))
    elif tile == "one":
        screen.blit(one_mine, (col*block_size*scale, row*block_size*scale))
    elif tile == "two":
        screen.blit(two_mines, (col*block_size*scale, row*block_size*scale))
    elif tile == "three":
        screen.blit(three_mines, (col*block_size*scale, row*block_size*scale))
    elif tile == "four":
        screen.blit(four_mines, (col*block_size*scale, row*block_size*scale))
    elif tile == "five":
        screen.blit(five_mines, (col*block_size*scale, row*block_size*scale))
    elif tile == "six":
        screen.blit(six_mines, (col*block_size*scale, row*block_size*scale))
    elif tile == "seven":
        screen.blit(seven_mines, (col*block_size*scale, row*block_size*scale))
    elif tile == "eight":
        screen.blit(eight_mines, (col*block_size*scale, row*block_size*scale))
    elif tile == "green":
        pygame.draw.rect(screen, 
                        (0, 255, 0), 
                        pygame.Rect(col*block_size*scale, row*block_size*scale, 
                                    block_size*scale, block_size*scale))
    elif tile == "red":
        pygame.draw.rect(screen, 
                        (255, 0, 0), 
                        pygame.Rect(col*block_size*scale, row*block_size*scale, 
                                    block_size*scale, block_size*scale))
    else:
        raise RuntimeError("Invalid tile type")


if __name__ == "__main__":
    main(8, 8, 3)


