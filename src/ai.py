import copy
import math
import multiprocessing
import pickle
#from game import *
from move import Move
from board import Board
from const import *
from piece import Pawn
from square import Square


class AI:
    def __init__(self):
        self.eval = -9999
        
    @staticmethod      
    def eval_board(board):
        value = 0
        for row in range(ROWS):
            for col in range(COLS):
                if board.square[row][col].has_piece():
                    value += board.square[row][col].piece.value
                    
        return value

    @staticmethod
    def minimax(board, depth, game, white=True):
        if game.game_over or depth == 0:
           return [AI.eval_board(board), None]
       
        if white:
            bestMove = None
            bestVal = -math.inf
            temp_board = copy.deepcopy(board)
            for row in range(ROWS):
                for col in range(COLS):
                    if board.square[row][col].has_team_piece('white'):
                        p = copy.deepcopy(board.square[row][col].piece)
                        board.calc_moves(p,row, col)
                        for m in p.moves:
                            temp_board2 = copy.deepcopy(temp_board)
                            temp_board2.move(p,m)
                            value = AI.minimax(temp_board2, depth-1, game, False)[0]
                            if value > bestVal:
                                bestVal = value
                                bestMove = m
            print([bestVal])
            return [bestVal,bestMove]
        
        else:
            bestMove = None
            bestVal = -math.inf
            temp_board = copy.deepcopy(board)
            for row in range(ROWS):
                for col in range(COLS):
                    if board.square[row][col].has_team_piece('black'):
                        p = copy.deepcopy(board.square[row][col].piece)
                        board.calc_moves(p,row, col)
                        for m in p.moves:
                            temp_board2 = copy.deepcopy(temp_board)
                            temp_board2.move(p,m)
                            value = AI.minimax(temp_board2, depth-1, game, True)[0]
                            if value > bestVal:
                                bestVal = value
                                bestMove = m
            print([bestVal])
            return [bestVal,bestMove]
        
    @staticmethod
    def best_ai_move(board, game):
        bestVal = -math.inf
        bestMove = None
        temp_board = copy.deepcopy(board)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.square[row][col].has_team_piece('white'):
                    p = copy.deepcopy(temp_board.square[row][col].piece)
                    temp_board.calc_moves(p,row,col)
                    for m in p.moves:
                        
                        temp_board2 = copy.deepcopy(board)
                        temp_board2.move(p,m)
                        value = AI.minimax(temp_board2, 2,game, False)[0]
                        if value > bestVal:
                            bestVal = value
                            bestMove = m
                            
        if bestMove and board.square[bestMove.initial.row][bestMove.initial.col].has_piece():
            piece = board.square[bestMove.initial.row][bestMove.initial.col].piece
            print(piece.name, bestVal)
            board.move(piece, bestMove)
            
            
    #alpha beta pruning         
    @staticmethod
    def alpha_beta(board, depth, alpha, beta, game, white):
        
        if depth == 0 or board.game_is_over():
            #board.print_board()
            return [board.calc_value_of_board(), None]
            
        #checking possible moves for white
        if white:
            condition = True
            bestMove = None
            temp_board = copy.deepcopy(board)
            for row in range(ROWS):
                if not condition:
                    break
                for col in range(COLS):
                    if not condition:
                        break
                    if board.square[row][col].has_team_piece('white'):
                        p = copy.deepcopy(board.square[row][col].piece)
                        temp_board.calc_moves(p,row, col)
                        for m in p.moves:
                            temp_board2 = copy.deepcopy(temp_board)
                            temp_board2.move(p,m,testing=True)
                            value = AI.alpha_beta(temp_board2, depth-1, alpha,beta,game,False)[0]
                            if value > alpha:
                                alpha = value
                                bestMove = m
                            if alpha >= beta:
                                condition = False
                                break
            #print("alpha",[alpha])
            return [alpha, bestMove]
        
        else:
            condition = True
            bestMove = None
            temp_board = copy.deepcopy(board)
            for row in range(ROWS):
                if not condition:
                    break
                for col in range(COLS):
                    if not condition:
                        break
                    if board.square[row][col].has_team_piece('black'):
                        p = copy.deepcopy(board.square[row][col].piece)
                        temp_board.calc_moves(p,row, col)
                        for m in p.moves:
                            temp_board2 = copy.deepcopy(temp_board)
                            temp_board2.move(p,m,testing=True)
                            
                            value = AI.alpha_beta(temp_board2, depth-1, alpha,beta,game,True)[0]
                            if value < beta:
                                beta = value
                                bestMove = m
                            if alpha >= beta:
                                condition = False
                                break
            #print("beta",[beta])
            
            return [beta, bestMove]
    
    
    #slow for white
    @staticmethod
    def ai_best_move_ab(board, game):
        bestVal = -math.inf
        bestMove = None
        alpha = -math.inf
        beta = math.inf
        
        temp_board = copy.deepcopy(board)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.square[row][col].has_team_piece('white'):
                    p = copy.deepcopy(temp_board.square[row][col].piece)
                    temp_board.calc_moves(p,row,col)
                    for m in p.moves:
                        
                        temp_board2 = copy.deepcopy(board)
                        temp_board2.move(p,m,testing=True)
                        value = AI.alpha_beta(temp_board2, 2,alpha, beta, game, False)[0]
                        if value > bestVal:
                            bestVal = value
                            bestMove = m
                        alpha = max(alpha, bestVal)
                            
        if bestMove and board.square[bestMove.initial.row][bestMove.initial.col].has_piece():
            piece = board.square[bestMove.initial.row][bestMove.initial.col].piece
            print(piece.name, bestVal)
            board.move(piece, bestMove)
    
    #slow for black
    @staticmethod        
    def ai_best_move_ab_black(board, game):
        bestVal = math.inf
        bestMove = None
        alpha = -math.inf
        beta = math.inf
        
        temp_board = copy.deepcopy(board)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.square[row][col].has_team_piece('black'):
                    p = copy.deepcopy(temp_board.square[row][col].piece)
                    temp_board.calc_moves(p,row,col)
                    for m in p.moves:
                        
                        temp_board2 = copy.deepcopy(board)
                        temp_board2.move(p,m,testing=True)
                        value = AI.alpha_beta(temp_board2, 2,alpha, beta, game, True)[0]
                        if value < bestVal:
                            bestVal = value
                            bestMove = m
                        beta = min(beta, bestVal)
                            
        if bestMove and board.square[bestMove.initial.row][bestMove.initial.col].has_piece():
            piece = board.square[bestMove.initial.row][bestMove.initial.col].piece
            board.calc_moves(piece,bestMove.initial.row, bestMove.initial.col)
            board.move(piece, bestMove)
            board.set_true_en_passant(piece)
    
    #currently using
    @staticmethod
    def getBestMoveBlack(board, game):
        _,bestMove = AI.alpha_beta(board,3,-math.inf,math.inf,game,False )
        if bestMove and board.square[bestMove.initial.row][bestMove.initial.col].has_piece():
            piece = board.square[bestMove.initial.row][bestMove.initial.col].piece
            board.calc_moves(piece,bestMove.initial.row, bestMove.initial.col)
            board.move(piece, bestMove)
            board.set_true_en_passant(piece)
                         
    #negamax
    @staticmethod
    def negamax(board, depth, alpha, beta, color):
        
        if depth == 0 or board.game_is_over():
            #board.print_board()
            return [color*board.calc_value_of_board(), None]
        
        condition = True
        bestMove = None
        temp_board = copy.deepcopy(board)
        for row in range(ROWS):
            if not condition:
                break
            for col in range(COLS):
                if not condition:
                    break
                if board.square[row][col].has_piece():
                    p = copy.deepcopy(board.square[row][col].piece)
                    temp_board.calc_moves(p,row, col)
                    for m in p.moves:
                        temp_board2 = copy.deepcopy(temp_board)
                        temp_board2.move(p,m,testing=True)
                        print(-beta, -alpha)
                        value = -AI.negamax(temp_board2, depth-1,-beta, -alpha, -color)[0]
                        temp_board2 = copy.deepcopy(temp_board)
                        if value > alpha:
                            alpha = value
                            bestMove = m
                        if alpha >= beta:
                            condition = False
                            break
        #print("alpha",[alpha])
        return [alpha, bestMove]
         
    @staticmethod
    def negamax_black_2(board, depth):
        best_value = math.inf
        bestMove =None
        temp_board = copy.deepcopy(board)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.square[row][col].has_team_piece('black'):
                    p = copy.deepcopy(temp_board.square[row][col].piece)
                    temp_board.calc_moves(p,row,col)
                    for m in p.moves:
                        
                        temp_board2 = copy.deepcopy(board)
                        temp_board2.move(p,m,testing=True)
                        value = -AI.negamax(board,depth,-math.inf, math.inf, -1)[0]
                        if value < best_value:
                            bestMove = value
                            bestMove = m
                            
        
        if bestMove and board.square[bestMove.initial.row][bestMove.initial.col].has_piece():
            piece = board.square[bestMove.initial.row][bestMove.initial.col].piece
            board.calc_moves(piece,bestMove.initial.row, bestMove.initial.col)
            board.move(piece, bestMove)
            board.set_true_en_passant(piece)
        
    @staticmethod        
    def negamax_black(board, depth):
        bestVal,bestMove = AI.negamax(board, depth, alpha=-math.inf, beta=math.inf, color=-1)
        if bestMove and board.square[bestMove.initial.row][bestMove.initial.col].has_piece():
            piece = board.square[bestMove.initial.row][bestMove.initial.col].piece
            board.calc_moves(piece,bestMove.initial.row, bestMove.initial.col)
            print(piece.name, bestVal)
            board.move(piece, bestMove)
            board.set_true_en_passant(piece)
    
    