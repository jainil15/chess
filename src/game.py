import os
from ai import AI
from config import Config
from piece import King
import pygame

from dragger import *
from board import Board
from const import *
from square import Square


class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered = False
        self.board = Board()
        self.dragger = Dragger()
        self.hovered_sqr = None
        self.config = Config()
        self.game_over = False
        self.winner = ''
        self.draw = False

    # show methods
    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                #color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                #rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
                
                if col == 0:
                    #create a new color
                    color = theme.bg.dark if row %2 == 0 else theme.bg.light
                    #label
                    label = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (WIDTH//160,(WIDTH//160)+row*SQSIZE)
                    #blit
                    surface.blit(label,lbl_pos)
                
                if row == 7:
                    #create a new color
                    color = theme.bg.dark if (row +col )%2 == 0 else theme.bg.light
                    #label
                    label = self.config.font.render(Square.get_alpha(col), 1, color)
                    lbl_pos = (col*SQSIZE+SQSIZE-(HEIGHT//40),HEIGHT-(HEIGHT//40))
                    #blit
                    surface.blit(label,lbl_pos)
                    

    def show_pieces(self, surface):
        
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.square[row][col].has_piece():
                    piece = self.board.square[row][col].piece

                    if piece is not self.dragger.piece:
                        if isinstance(piece,King) and piece.check:
                            img = pygame.image.load(os.path.join(f'C:/PDF/chess/assets/piece_png/check_.png'))
                            img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                            piece.texture_rect = img.get_rect(center=img_center)
                            surface.blit(img, piece.texture_rect)
                            
                        piece.set_texture(size=96)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
                
                    
    def show_moves(self, surface):
        theme = self.config.theme
        
        if self.dragger.dragging:
            piece = self.dragger.piece
            
            #loop all valid moves
            for move in piece.moves:
                #color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                
                #rect or circ
                rect = (move.final.col*SQSIZE, move.final.row*SQSIZE, SQSIZE,SQSIZE)
                #circ = ((move.final.col*SQSIZE)+SQSIZE//2, (move.final.row*SQSIZE)+SQSIZE//2)
                #blit
                #pygame.draw.circle(surface, color, circ, SQSIZE//6)
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface):
        #print(self.board.last_move.initial.row, self.board.last_move.initial.col)
        if self.board.last_move:
            theme = self.config.theme
            
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial, final]:
                #color
                color = theme.trace.light if (pos.row + pos.col) % 2==0 else theme.trace.dark
                #rect or circ
                rect = (pos.col*SQSIZE, pos.row*SQSIZE, SQSIZE, SQSIZE)

                #blit
                pygame.draw.rect(surface, color, rect)
    
    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180,180,180)
            
            #rect or circ
            rect = (self.hovered_sqr.col*SQSIZE, self.hovered_sqr.row*SQSIZE, SQSIZE, SQSIZE)

            #blit
            pygame.draw.rect(surface, color, rect, width=3)
    
    
    #other methods
    
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        self.board.king_is_in_check()
        self.winner = 'white' if self.next_player == 'black' else 'black'
        if  self.board.check_mate(self.next_player) == (True, False):
            self.draw = True
            self.game_over = True
            
        elif self.board.check_mate(self.next_player) == (True, True):
            
            self.game_over = True
            
        elif self.board.king_2_stalemate():
            self.draw = True
            self.game_over = True
            
        else:
            self.game_over = False
            
        print(self.board.calc_value_of_board())
        
        
        
        
       
    def set_hover(self, row, col):
        if row < 8 and col < 8:
            self.hovered_sqr = self.board.square[row][col]
        
    def change_theme(self):
        self.config.change_theme()
        
    def play_sound(self, captured=False, check=False):
        if captured and not check:
            self.config.capture_sound.play()
        elif check:
            self.config.check_sound.play()
        else:
            self.config.move_sound.play()
    
    def reset(self):
        self.__init__()
        
    def _game_over(self, surface):
        if self.game_over:
            color1 = (23,22,99)
            color2 = (123,122,199)
            rect = (HEIGHT//2-125, WIDTH//2-50, 300, 100)
            pygame.draw.rect(surface, color2, rect)
            if self.draw:
                self.render_multi_line(surface, "GAME OVER\nSTALEMATE\nclick r to restart", WIDTH//2-125, HEIGHT//2-50 , 28, color1)
                return
            self.render_multi_line(surface, f"GAME OVER\n{self.winner} WON\nclick r to restart", WIDTH//2-125, HEIGHT//2-50 , 28, color1)
            
            #label = self.config.uifont.render("GAME OVER\nSTALEMATE\nclick r to restart",1,color1)
            #lbl_pos = (HEIGHT//2-75, WIDTH//2-15)
            #surface.blit(label,lbl_pos)
            
    def render_multi_line(self,surface,text, x, y, fsize, hecolor):
        lines = text.splitlines()
        for i, l in enumerate(lines):
            surface.blit(self.config.uifont.render(l, 1, hecolor), (x, y + fsize*i))