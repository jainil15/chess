from const import *
from move import *
from square import Square
from piece import *


class Board:
    def __init__(self):
        self.square = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.last_move = None
    
    def move(self, piece, move):
        initial = move.initial
        final = move.final
        
        #console board move update
        self.square[initial.row][initial.col].piece = None
        self.square[final.row][final.col].piece = piece
        
        #moved
        piece.moved = True
        
        #clear valid moves
        piece.clear_moves()
        
        #set last move
        self.last_move = move
        
    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):
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
                        final = Square(possible_move_row, possible_move_col)

                        # create new move
                        move = Move(initial, final)

                        # append new Move
                        piece.add_move(move)

            move_row = row + piece.dir

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
                        final = Square(possible_move_row, possible_move_col)
                        # move new move
                        move = Move(initial, final)
                        # append new valid move
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
                        final = Square(possible_move_row, possible_move_col)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.square[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)

                        # has enemy piece = break
                        if self.square[possible_move_row][
                            possible_move_col
                        ].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break

                        # has team piece
                        if self.square[possible_move_row][
                            possible_move_col
                        ].has_team_piece(piece.color):
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
            
            #normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.square[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        
                        #create sqaures of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        
                        #create new move
                        move = Move(initial, final)
                        
                        #append new valid move
                        piece.add_move(move)
                        
            #castling moves
                
                
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

        # pawns
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
