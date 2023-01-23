import pygame

from dragger import *
from board import Board
from const import *


class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered = False
        self.board = Board()
        self.dragger = Dragger()
        self.hovered_sqr = None

    # show methods
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)  # light green color
                else:
                    color = (119, 154, 88)  # dark green color

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.square[row][col].has_piece():
                    piece = self.board.square[row][col].piece
                    

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=64)
                        img = pygame.image.load(piece.texture)
                        img = pygame.transform.smoothscale(img, (1,1))
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            
            #loop all valid moves
            for move in piece.moves:
                #color
                color = '#d3d3d3' if (move.final.row + move.final.col) % 2 == 0 else '#9e9e9e'
                
                #rect or circ
                rect = (move.final.col*SQSIZE, move.final.row*SQSIZE, SQSIZE,SQSIZE)
                #circ = ((move.final.col*SQSIZE)+SQSIZE//2, (move.final.row*SQSIZE)+SQSIZE//2)
                
                #blit
                #pygame.draw.circle(surface, color, circ, SQSIZE//6)
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface):
        #print(self.board.last_move.initial.row, self.board.last_move.initial.col)
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            
            for pos in [initial, final]:
                #color
                
                color = (244, 247, 116) if (pos.row + pos.col) % 2==0 else (172,195,51)
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
       
    def set_hover(self, row, col):
        self.hovered_sqr = self.board.square[row][col]