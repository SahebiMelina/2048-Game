import pygame   #main library for our game
import random   #to give us random numbers
import math     #to perform mathematical operations

pygame.init()   #initialize all pygame modules
FPS = 60    #frames_per_second               #All data we need to have
WIDTH , HEIGHT = 800 , 800  #window dimensions in pixels
ROWS = 4   #no. of rows
COLS = 4   #no. of columns
RECT_HEIGHT = HEIGHT // ROWS    #height of each cell
RECT_WIDTH = WIDTH // COLS      #width of each cell
OUTLINE_COLOR = (187,173,160)   #all colors for appearance
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205,192,180)
FONT_COLOR = (119,110,101)
FONT = pygame.font.SysFont("comicsans",60,bold=True)  #font style
MOVE_VEL = 20 #speed of tile movement
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT)) #the way it shows us the window
pygame.display.set_caption("2048") #the title of the window


class Tile :
    COLORS = [  #color palette
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self,value,row,column):
        self.value = value #tiles's numbers
        self.row = row #grid's rows
        self.column = column #grid's columns
        self.x = column*RECT_WIDTH #x's pixel
        self.y = row*RECT_HEIGHT #y's pixel

    def get_color(self): #determine tile's color based on its value
        color_index = int(math.log2(self.value))-1 #calculate index
        color = self.COLORS[color_index]  #select from colores's tuple
        return color
    
    def draw(self,window): #draw our rectangle
        color = self.get_color()
        pygame.draw.rect(window,color,(self.x,self.y,RECT_WIDTH,RECT_HEIGHT)) #1st we should draw the rect otherwise the text ould be hidden
        text = FONT.render(str(self.value),1,FONT_COLOR)
        window.blit( #position the text
               text,
               (
                self.x + (RECT_WIDTH/2 - text.get_width() / 2), #center x
                self.y + (RECT_HEIGHT/2 - text.get_height() / 2), #center y
                ),
            )
        pass
    def set_position(self,ceil=False):
        if ceil: #if we are going up
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.column = math.ceil(self.x / RECT_WIDTH)
        else : #if we go down 
            self.row = math.floor(self.y / RECT_HEIGHT) 
            self.column = math.floor(self.x / RECT_WIDTH)  
        
    def move(self,delta):
        self.x += delta[0] 
        self.y += delta[1] 

def set_board(window):    #draw_board
    for row in range(1,ROWS):  #draw horizontal lines
        y = row * RECT_HEIGHT
        pygame.draw.line(window,OUTLINE_COLOR,(0,y),(WIDTH,y),OUTLINE_THICKNESS)

    for column in range(1,COLS): #draw vertical lines
        x = column * RECT_WIDTH
        pygame.draw.line(window,OUTLINE_COLOR,(x,0),(x,HEIGHT),OUTLINE_THICKNESS)    
    pygame.draw.rect(window,OUTLINE_COLOR,(0,0,WIDTH,HEIGHT),OUTLINE_THICKNESS)

def draw(window,tiles):
    window.fill(BACKGROUND_COLOR)
    set_board(window)
    for tile in tiles.values():
        tile.draw(window)
    pygame.display.update()

def get_random_position(tiles):
    row = None
    column = None
    while True:
        row = random.randrange(0,ROWS)
        column = random.randrange(0,COLS)
        if f"{row}{column}" not in tiles:
            break
    return row,column    

def move_tiles(window,tiles,clock,direction):
    updated = True
    blocks = set()
    if direction =="left":
        sort_func = lambda x : x.column #sort the tiles by their column
        reverse = False
        delta = (-MOVE_VEL,0) #move in the x direction to the left
        boundary_check = lambda tile : tile.column == 0 #move as left as possible
        get_next_tile = lambda tile : tiles.get(f"{tile.row}{tile.column - 1}") #the tile to our left if it didn't exist it returns none
        merge_check = lambda tile , next_tile : tile.x > next_tile.x + MOVE_VEL 
        move_check =  lambda tile , next_tile : tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True #should we go up or down after we moved the tile

    elif direction == "right":
        sort_func = lambda x : x.column #sort the tiles by their column
        reverse = True
        delta = (MOVE_VEL,0) #move in the x direction to the right
        boundary_check = lambda tile : tile.column == COLS - 1 #move as right as possible
        get_next_tile = lambda tile : tiles.get(f"{tile.row}{tile.column + 1}") #the tile to our right if it didn't exist it returns none
        merge_check = lambda tile , next_tile : tile.x < next_tile.x - MOVE_VEL 
        move_check =  lambda tile , next_tile : tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False #should we go up or down after we moved the tile
        
    elif direction == "up" :
        sort_func = lambda x : x.row  #sort the tiles by their row
        reverse = False
        delta = (0,-MOVE_VEL) #move in the x direction uppward
        boundary_check = lambda tile : tile.row == 0 #move as uppward as possible
        get_next_tile = lambda tile : tiles.get(f"{tile.row-1}{tile.column}") #the upper tile didn't exist it returns none
        merge_check = lambda tile , next_tile : tile.y > next_tile.y + MOVE_VEL 
        move_check =  lambda tile , next_tile : tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True #should we go up or down after we moved the tile

    elif direction == "down":
        sort_func = lambda x : x.row  #sort the tiles by their row
        reverse = True
        delta = (0,MOVE_VEL) #move in the x direction downward
        boundary_check = lambda tile : tile.row == ROWS - 1 #move as uppward as possible
        get_next_tile = lambda tile : tiles.get(f"{tile.row+1}{tile.column}") #the upper tile didn't exist it returns none
        merge_check = lambda tile , next_tile : tile.y < next_tile.y - MOVE_VEL 
        move_check =  lambda tile , next_tile : tile.y+ RECT_HEIGHT + MOVE_VEL  < next_tile.y 
        ceil = False #should we go up or down after we moved the tile
        
    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(),key=sort_func,reverse=reverse)
        
        for i,tile  in enumerate(sorted_tiles): #get the index and the tile itself
            if boundary_check(tile):  #if we are already at the boundary we are not able to move
                continue
            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile,next_tile): #1st check if we can merge the 2 tiles
                    tile.move(delta)
                else :
                    next_tile.value *= 2
                    sorted_tiles.pop(i)  
                    blocks.add(next_tile)
            elif move_check(tile,next_tile):
                tile.move(delta)
            else :
                continue


            tile.set_position(ceil)
            updated = True                 
        update_tiles(window,tiles,sorted_tiles)

    return board_completed(tiles)

def board_completed(tiles):
    if len(tiles) == 16:
        return "Lost"
    row , column = get_random_position(tiles)  
    tiles[f"{row}{column}"] = Tile(random.choice([2,4]),row,column)
    return "continue" 

def update_tiles(window,tiles,sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.column}"] = tile

    draw (window,tiles)           


def fill_board():
    tiles = {}
    for _ in range(2) : #do it twice so that we pick both row and column
        row,column = get_random_position(tiles) #do it randomly not to pick any repeated tile
        tiles[f"{row}{column}"]=Tile(2,row,column)
    return tiles    

def main(window):   #handle_game_events
    clock = pygame.time.Clock()
    run = True
    tiles = fill_board() #we use dict for instant access to a tile's row and column indexes
    while run:
        clock.tick(FPS) #handles game speed
        for event in pygame.event.get(): #handle the events
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT :
                    move_tiles(window,tiles,clock,"left")
                if event.key == pygame.K_RIGHT :
                    move_tiles(window,tiles,clock,"right")
                if event.key == pygame.K_UP :
                    move_tiles(window,tiles,clock,"up") 
                if event.key == pygame.K_DOWN :
                    move_tiles(window,tiles,clock,"down")           
                
        draw(window,tiles)    
    pygame.quit()        
if __name__ == '__main__':
    main(WINDOW)
