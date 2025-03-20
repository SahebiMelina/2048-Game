
import numpy as np
import pygame
import random
import sys

WIDTH, HEIGHT = 478, 532
BOARD_WIDTH, BOARD_HEIGHT = 280, 280
COLS, ROWS = 4, 4
XSHIFT, XSHIFT2, XSHIFT3 = 100, 197, 264
YSHIFT, YSHIFT2, YSHIFT3 = 20, 85, 144
GAP = 8
TILE_SIZE = (280 - 5 * GAP)//4

WHITE = (255, 255, 255)

SCREEN_COLOR = (249, 246, 235)
BOARD_COLOR = (173, 157, 143)

GAMEOVER_LBL_COLOR = (119, 111, 102)
TRANSPARENT_ALPHA = 210

TILES_COLORS = {
    0: (194, 178, 166),
    2: (233, 221, 209),
    4: (232, 217, 189),
    8: (236, 161, 101),
    16: (241, 130, 80),
    32: (239, 100, 77),
    64: (240, 69, 45),
    128: (230, 197, 94),
    256: (227, 190, 78),
    512: (230, 189, 64),
    1024: (233, 185, 49),
    2048: (233, 187, 32),
    4096: (35, 32, 29),
    8192: (35, 32, 29),
}

LBLS_COLORS = {
    0: (194, 178, 166),
    2: (99, 91, 82),
    4: (99, 91, 82),
    8: WHITE,
    16: WHITE,
    32: WHITE,
    64: WHITE,
    128: WHITE,
    256: WHITE,
    512: WHITE,
    1024: WHITE,
    2048: WHITE,
    4096: WHITE,
    8192: WHITE,
}
class ScoreManager:

    def __init__(self):
        self.score = 0
        self.best = 0
        
    def check_highscore(self):
        if self.score >= self.best:
            self.best = self.score

    def reset_score(self):
        self.score = 0

class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.transparent_screen = pygame.Surface( (BOARD_WIDTH, BOARD_HEIGHT) )
        self.transparent_screen.set_alpha( TRANSPARENT_ALPHA )
        self.transparent_screen.fill( WHITE )

        
        self.go_font = pygame.font.SysFont('verdana', 30, True)
        self.go_lbl = self.go_font.render('Game over!', 1, GAMEOVER_LBL_COLOR)
        self.go_pos = (XSHIFT + BOARD_WIDTH//2 - self.go_lbl.get_rect().width//2, YSHIFT3 + BOARD_HEIGHT//2 - self.go_lbl.get_rect().height//2 - 35)

      
        self.tryagain_btn = pygame.image.load('tryagain_btn.png')
        self.tryagain_btn = pygame.transform.scale(self.tryagain_btn, (115, 40))
        self.tryagain_btn_pos = (XSHIFT + BOARD_WIDTH//2 - self.tryagain_btn.get_width()//2, YSHIFT3 + BOARD_HEIGHT//2 - self.tryagain_btn.get_height()//2 + 35)
        self.tryagain_btn_rect = self.tryagain_btn.get_rect(topleft=self.tryagain_btn_pos)

      
        self.active = False
        
    def show(self):
        if self.active:
            
            self.screen.blit(self.transparent_screen, (XSHIFT, YSHIFT3))

            
            self.screen.blit(self.go_lbl, self.go_pos)

            
            self.screen.blit(self.tryagain_btn, self.tryagain_btn_pos)

    def hide(self, bg):
        self.active = False

        pygame.draw.rect(self.screen, BOARD_COLOR, bg)

class GUI:

    def __init__(self, screen):
      
        self.screen = screen

        self.logo = pygame.image.load('logo.png')
        self.logo = pygame.transform.scale(self.logo, (self.logo.get_width()//2, self.logo.get_height()//2))
        self.logo_pos = (XSHIFT, YSHIFT)

        self.score_rect = pygame.image.load('score_rect.png')
        self.score_rect = pygame.transform.scale(self.score_rect, (90, 42))
        self.score_rect_pos = (XSHIFT2, YSHIFT)
        
        self.best_rect = pygame.image.load('best_rect.png')
        self.best_rect = pygame.transform.scale(self.best_rect, (90, 42))
        self.best_rect_pos = (XSHIFT2 + self.score_rect.get_width() + 2, YSHIFT)

        self.score_font = pygame.font.SysFont('verdana', 15, bold=True)

        self.menu_btn = pygame.image.load('menu_btn.png')
        self.menu_btn = pygame.transform.scale(self.menu_btn, (self.menu_btn.get_width()//2, self.menu_btn.get_height()//2))
        self.menu_btn_pos = (XSHIFT, YSHIFT2)

        self.newgame_btn = pygame.image.load('newgame_btn.png')
        self.newgame_btn = pygame.transform.scale(self.newgame_btn, (115, 40))
        self.newgame_btn_pos = (XSHIFT3, YSHIFT2)
        self.newgame_btn_rect = self.newgame_btn.get_rect(topleft=self.newgame_btn_pos)

        
        self.board_rect = (XSHIFT, YSHIFT3, BOARD_WIDTH, BOARD_HEIGHT)

        self.menu = Menu( screen )

    def show_start(self):
        self.screen.blit(self.logo, self.logo_pos)
        self.screen.blit(self.score_rect, self.score_rect_pos)
        self.screen.blit(self.best_rect, self.best_rect_pos)
        self.screen.blit(self.menu_btn, self.menu_btn_pos)
        self.screen.blit(self.newgame_btn, self.newgame_btn_pos)
        pygame.draw.rect(self.screen, BOARD_COLOR, self.board_rect)

    def update_scores(self, score_value, best_value):
        self.screen.blit(self.score_rect, self.score_rect_pos)
        self.score_lbl = self.score_font.render(str(score_value), 0, WHITE)
        self.score_pos = (XSHIFT2 + self.score_rect.get_width()//2 - self.score_lbl.get_rect().width//2, YSHIFT + self.score_rect.get_height()//2 - self.score_lbl.get_rect().height//2 + 8)
        self.screen.blit(self.score_lbl, self.score_pos)
        self.screen.blit(self.best_rect, self.best_rect_pos)
        self.best_lbl = self.score_font.render(str(best_value), 0, WHITE)
        self.best_pos = (290 + self.best_rect.get_width()//2 - self.best_lbl.get_rect().width//2, YSHIFT + self.best_rect.get_height()//2 - self.best_lbl.get_rect().height//2 + 8)
        self.screen.blit(self.best_lbl, self.best_pos)

    def action_listener(self, event):
        if self.menu.active:
            if self.menu.tryagain_btn_rect.collidepoint(event.pos):
                self.menu.hide(self.board_rect)
                return True
        elif self.newgame_btn_rect.collidepoint(event.pos):
            return True
        return False

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.tiles = np.zeros( (ROWS, COLS) )
        self.gui = GUI(screen)
        self.score_manager = ScoreManager()
        self.lbl_font = pygame.font.SysFont('verdana', 30, bold=True)
        self.generate = False
        self.playing = True

    def draw_board(self):
        rShift, cShift = GAP, GAP
        for row in range(ROWS):
            for col in range(COLS):
                tile_num = int(self.tiles[row][col])
                tile_color = TILES_COLORS[tile_num]
                pygame.draw.rect(self.screen, tile_color, (XSHIFT + cShift + col * TILE_SIZE, YSHIFT3 + rShift + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                tile_lbl_color = LBLS_COLORS[tile_num]
                lbl = self.lbl_font.render(str(tile_num), 0, tile_lbl_color)
                lbl_pos = (XSHIFT + cShift + col * TILE_SIZE + TILE_SIZE//2 - lbl.get_rect().width//2, YSHIFT3 + rShift + row * TILE_SIZE + TILE_SIZE//2 - lbl.get_rect().height//2)
                self.screen.blit(lbl, lbl_pos)

                cShift += GAP
            rShift += GAP
            cShift = GAP

    def generate_tiles(self, first=False):
        empty_tiles = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == 0: empty_tiles.append( (row, col) )
        idx = random.randrange(0, len(empty_tiles))
        row, col = empty_tiles[idx]
        rnd = random.randint(1, 10)
        tile_value = 2
        if not first and rnd > 7: tile_value = 4
        self.tiles[row][col] = tile_value

    def __move_and_merge(self, direction, row, col):
        dx, dy = 0, 0
        if direction == 'UP': dy = -1
        elif direction == 'DOWN': dy = 1
        elif direction == 'RIGHT': dx = 1
        elif direction == 'LEFT': dx = -1
        try:
            if self.tiles[row + dy][col + dx] == 0:
                value = self.tiles[row][col]
                self.tiles[row][col] = 0
                self.tiles[row + dy][col + dx] = value
                self.generate = True
                self.__move_and_merge(direction, row + dy, col + dx)
            elif self.tiles[row][col] == self.tiles[row + dy][col + dx]:
                self.tiles[row][col] = 0
                self.tiles[row + dy][col + dx] *= 2
                self.score_manager.score += int(self.tiles[row + dy][col + dx])
                self.generate = True
        except IndexError: return

    def slide_tiles(self, direction):
        if direction == 'UP':
            for row in range(1, ROWS):
                for col in range(COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)
        if direction == 'DOWN':
            for row in range(ROWS-2, -1, -1):
                for col in range(COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)
        if direction == 'RIGHT':
            for row in range(ROWS):
                for col in range(COLS-2, -1, -1):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)
        if direction == 'LEFT':
            for row in range(ROWS):
                for col in range(1, COLS):
                    if self.tiles[row][col] != 0: self.__move_and_merge(direction, row, col)

    def __full_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == 0: return False
        return True

    def __no_more_moves(self):
        for row in range(1, ROWS):
            for col in range(COLS):
                if self.tiles[row][col] == self.tiles[row-1][col]: return False
        for row in range(ROWS-2, -1, -1):
            for col in range(COLS):
                if self.tiles[row][col] == self.tiles[row+1][col]: return False
        for row in range(ROWS):
            for col in range(COLS-2, -1, -1):
                if self.tiles[row][col] == self.tiles[row][col+1]: return False
        for row in range(ROWS):
            for col in range(1, COLS):
                if self.tiles[row][col] == self.tiles[row][col-1]: return False
        return True

    def is_game_over(self):
        if self.__full_board():
            return self.__no_more_moves()
    
    def new(self):
        self.tiles = np.zeros( (ROWS, COLS) )
        self.score_manager.reset_score()
        self.generate_tiles()

def main():
    pygame.init()
    screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
    pygame.display.set_caption('2048')
    screen.fill( SCREEN_COLOR )
    game = Game(screen)
    game.gui.show_start()
    for i in range(2): game.generate_tiles(True)
    while game.playing:
        game.draw_board()
        game.gui.menu.show()
        game.gui.update_scores(game.score_manager.score, game.score_manager.best)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.slide_tiles('UP')
                if event.key == pygame.K_DOWN:
                    game.slide_tiles('DOWN')
                if event.key == pygame.K_RIGHT:
                    game.slide_tiles('RIGHT')
                if event.key == pygame.K_LEFT:
                    game.slide_tiles('LEFT')
                if game.generate:
                    game.generate_tiles()
                    game.generate = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game.gui.action_listener(event):
                        game.new()

        if game.is_game_over():
            game.gui.menu.active = True
        
        game.score_manager.check_highscore()
        
        pygame.display.update()

main()