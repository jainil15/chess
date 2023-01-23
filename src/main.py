from move import Move
import pygame
import sys
from const import *
from game import Game
from square import Square


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board

        while True:
            #show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    dragger.update_mouse(event.pos)
                    clicked_row = (dragger.mouseY // SQSIZE)
                    clicked_col = (dragger.mouseX // SQSIZE)

                    if board.square[clicked_row][clicked_col].has_piece():
                        piece = board.square[clicked_row][clicked_col].piece
                        #if piece.color = next_turn color
                        if piece.color == game.next_player:
                            
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            
                            #show methods
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            
                        
                # mouse button
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    
                    game.set_hover(motion_row, motion_col)
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        #show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                    
                        
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        
                        #create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                    
                        #valid move or not ?
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                           
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()
                        else:
                            piece.clear_moves() 
                            
                        
                    dragger.undrag_piece()

                # quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
