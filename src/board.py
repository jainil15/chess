import os
import copy
from const import *
from move import *
from sound import Sound
from square import Square
from piece import *


class Board:
    def __init__(self):
        self.square = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.last_move = None

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.square[final.row][final.col].isempty()
        # console board move update
        self.square[initial.row][initial.col].piece = None
        self.square[final.row][final.col].piece = piece
        
        
        
        
        if isinstance(piece, Pawn):
            #enpassant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update for en passant
                
                self.square[initial.row][initial.col + diff].piece = None
                self.square[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(
                        os.path.join('assets/sound/standard/Capture1.mp3')
                    )
                    sound.play()
        
            
            else:
                # pawn promotion
                self.check_promotion(piece, final)

        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])
        # moved
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move
        
        #self._print_moves(self.last_move, testing)
    
    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.square[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
                return
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.square[row][col].piece, Pawn):
                    self.square[row][col].piece.en_passant = False
                    
        piece.en_passant = True
                   
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        for row in range(ROWS):
            for col in range(COLS):
                 
                if temp_board.square[row][col].has_enemy_piece(piece.color):
                    
                    p = temp_board.square[row][col].piece
                    
                    temp_board.calc_moves(p, row, col, bool=False)
                    
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calc_moves(self, piece, row, col, bool=True):
        """
        calculates all the valid moves of a specific piece on a specific position
        """

        def pawn_moves():

            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.square[possible_move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)

                        # create new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.square[possible_move_row][possible_move_col].has_enemy_piece(piece.color):

                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.square[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        # create new move
                        move = Move(initial, final)

                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            #move_row = row + piece.dir
            
            #en passant
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            #left enpassant
            if Square.in_range(col-1) and row == r:
                if self.square[row][col-1].has_enemy_piece(piece.color):
                    p = self.square[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final_piece = self.square[row][col-1].piece
                            final = Square(fr, col-1, p)

                            # create new move
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece, move) :
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

            #right enpassant
            if Square.in_range(col+1) and row == r:
                if self.square[row][col+1].has_enemy_piece(piece.color):
                    p = self.square[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares
                            initial = Square(row, col)
                            final_piece = self.square[row][col+1].piece
                            final = Square(fr, col+1, p)

                            # create new move
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                                        
            
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row - 2, col - 1),
                (row - 2, col + 1),
                (row - 1, col - 2),
                (row - 1, col + 2),
                (row + 1, col - 2),
                (row + 1, col + 2),
                (row + 2, col - 1),
                (row + 2, col + 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.square[possible_move_row][
                        possible_move_col
                    ].isempty_or_enemy(piece.color):
                        # create square of a new move
                        initial = Square(row, col)
                        final_piece = self.square[possible_move_row][
                            possible_move_col
                        ].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # move new move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.square[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.square[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        # has enemy piece = break
                        elif self.square[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break

                        # has team piece
                        elif self.square[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    else:
                        break

                    # incementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                # up one row, left one column
                (row + 1, col - 1),
                # up one row, same column
                (row + 1, col),
                # up one row, right one column
                (row + 1, col + 1),
                # same row, left one column
                (row, col - 1),
                # same row, right one column
                (row, col + 1),
                # down one row, left one column
                (row - 1, col - 1),
                # down one row, same column
                (row - 1, col),
                # down one row, right one column
                (row - 1, col + 1),
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.square[possible_move_row][
                        possible_move_col
                    ].isempty_or_enemy(piece.color):

                        # create sqaures of the new move
                        initial = Square(row, col)
                        final_piece = self.square[possible_move_row][
                            possible_move_col
                        ].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        

                        # create new move
                        move = Move(initial, final)

                        # append new valid move
                        if bool:
                            if  not self.in_check(piece, move):
                                piece.add_move(move)
                                #print(f'{piece.color}{piece.name_initial}{Square.get_alpha(move.final.col)}{8-move.final.row} and {move.final.piece}')
                            
                        else:
                            piece.add_move(move)
                            
            # castling moves
            if not piece.moved:

                # queen castling
                left_rook = self.square[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.square[row][c].has_piece():
                                break
                            if c == 3:
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                #left_rook.add_move(moveR)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                
                                #initial = Square(row, 0)
                                #final = Square(row, 3)
                                #moveBtwn = Move()
                                
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR) and not self.in_check(piece, moveR):
                                        #append new move rook
                                        left_rook.add_move(moveR)
                                        #append new move king
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.square[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.square[row][c].has_piece():
                                break
                            if c == 6:
                                piece.right_rook = right_rook

                            # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                #right_rook.add_move(moveR)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR) and not self.in_check(piece, moveR):
                                        #append new move rook
                                        right_rook.add_move(moveR)
                                        #append new move king
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)
            else:
                if piece.right_rook:
                    piece.right_rook.clear_moves()
                if piece.left_rook:
                    piece.left_rook.clear_moves()

        # moves down here
        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves(
                [
                    (-1, 1),  # up-right
                    (-1, -1),  # up-left
                    (1, 1),  # down-right
                    (1, -1),  # down-left
                ]
            )

        elif isinstance(piece, Rook):
            straightline_moves(
                [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up  # right  # down  # left
            )

        elif isinstance(piece, Queen):
            straightline_moves(
                [
                    (-1, 1),  # up-right
                    (-1, -1),  # up-left
                    (1, 1),  # down-right
                    (1, -1),  # down-left
                    (-1, 0),  # up
                    (0, 1),  # right
                    (1, 0),  # down
                    (0, -1),  # left
                ]
            )

        elif isinstance(piece, King):

            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.square[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        #pawns
        for col in range(COLS):
           self.square[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.square[row_other][1] = Square(row_other, 1, Knight(color))
        self.square[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.square[row_other][2] = Square(row_other, 2, Bishop(color))
        self.square[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks

        self.square[row_other][0] = Square(row_other, 0, Rook(color))
        self.square[row_other][7] = Square(row_other, 7, Rook(color))

        # queens
        self.square[row_other][3] = Square(row_other, 3, Queen(color))

        # kings
        self.square[row_other][4] = Square(row_other, 4, King(color))
            


    #print moves
    def _print_moves(self, last_move, testing):
        if testing == False:
            print(f'{self.square[self.last_move.final.row][self.last_move.final.col].piece.name_initial}{Square.get_alpha(self.last_move.final.col)}{8-self.last_move.final.row}')
            
    def king_is_in_check(self):
        temp_board = copy.deepcopy(self)
        for row in range(ROWS):
            for col in range(COLS):
                p = temp_board.square[row][col].piece
                if isinstance(p, Piece):
                    temp_board.calc_moves(p, row, col, bool=False)
                    if isinstance(p, King):
                        setattr(self.square[row][col].piece,'check', False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            setattr(self.square[m.final.row][m.final.col].piece,'check', True)
                            return True
                    
        return False
    
    def _king_properties(self):
        temp_board = copy.deepcopy(self)
        for row in range(ROWS):
            for col in range(COLS):
                p = temp_board.square[row][col].piece
                if isinstance(p, King):
                    pass
                
    def check_mate(self, next_player_color):
        temp_board = copy.deepcopy(self)
        check_mate = True
        check = False
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.square[row][col].has_team_piece(next_player_color):
                    p = temp_board.square[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=True)
                    if isinstance(p, King):
                        check = p.check
                    if p.moves:
                        check_mate = False
                        return (check_mate, check)
        if check:
            check_mate = True
            print('checkmate')
            return (check_mate, check)
        else:
            check_mate = True
            print('stalemate')
            return (check_mate, check)
        
    def king_2_stalemate(self):
        temp_board = copy.deepcopy(self)
        kings = 0
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.square[row][col].has_piece():
                    if isinstance(temp_board.square[row][col].piece, King ):
                        kings += 1
                    else:
                        return False
            
        if kings == 2:
            return True
    def calc_value_of_board(self):
        value = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.square[row][col].has_piece():
                    p = self.square[row][col].piece
                    value += (p.value + p.pos_eval[row][col])
                    #print(p.name, p.value, p.pos_eval[row][col])
                    if isinstance(p, King):
                        if p.check and p.color == 'black':
                            if self.check_mate(p.color) == (True, True):
                                value += 10000
                            
                        elif p.check and p.color == 'white':
                            if self.check_mate(p.color) == (True, True):
                                value -= 10000
        return value
                        
                
    
    
                    
    def print_board(self):
        print('----------------------------------------------------------------')
        for row in range(ROWS):
            for col in range(COLS):
                if self.square[row][col].has_piece():
                    p = self.square[row][col].piece
                    print(f'{p.color}{p.name_initial}{Square.get_alpha(col)}{8-row}')
                    
    def game_is_over(self):
        if self.check_mate('white') == (True, True) or self.check_mate('black') == (True,True):
            return True
        
    def get_board_state(self):
        board_state = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.square[row][col].has_piece():
                    piece = self.square[row][col].piece
                    board_state.append([piece.color, piece.name, row, col])
        return board_state