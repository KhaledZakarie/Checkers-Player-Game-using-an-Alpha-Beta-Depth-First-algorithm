from copy import deepcopy   #create cope of object
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

#position is board
def minimax(position, depth, max_player, game, cond=float('inf')): #current board,how far of deping tree(evry call decrese the depth by1), max is bool if true we maximize
    if depth == 0 or position.winner() != None: #if we in depth zero(in leaf node) or ###
        return position.evaluate(), position    #return the evaluation of this board and the board (back track of recurtion)
    
    if max_player:          #if maximize the score
        maxEval = float('-inf') #max evaluation is -infinity
        best_move = None    #the best move
        for move in get_all_moves(position, WHITE, game):#loop in all alternative board
            evaluation = minimax(move, depth-1, False, game, maxEval)[0] #recall the method , and the evaluation = [0] (maxEval)
            if evaluation >= cond:
                break
            maxEval = max(maxEval, evaluation)  #maxeval = max of (old eva or new eva)
            if maxEval == evaluation:   #if the above line chose new eva is the max
                best_move = move        #best move is this board
        
        return maxEval, best_move   #return the maxi evaluation and the best board as [0][1]
    else:           #if minimize the score
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game, minEval)[0]
            if evaluation <= cond:
                break
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):  #truing make valid move of this piece in imagin board with his skipped
    board.move(piece, move[0], move[1]) #move piece to row,col
    if skip:    #if exist skiped piece
        board.remove(skip)  #remove the skiped piece

    return board    #RETURN board after do the valid move and skippe


def get_all_moves(board, color, game):  #get all move we can move to
    moves = []  #list of all board after do all valid moves

    for piece in board.get_all_pieces(color):   #loop on all piece of this color in the old board
        valid_moves = board.get_valid_moves(piece)  #get valid moves for all pieces color  {valid move : skipped pieces}
        for move, skip in valid_moves.items():  #loop on all valid move and skipped piece of this move
            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)    #copy of the board with the same positions
            temp_piece = temp_board.get_piece(piece.row, piece.col)     #the position will Guess his move
            new_board = simulate_move(temp_piece, move, temp_board, game, skip) #is new board after do the valid move and skippe
            moves.append(new_board) #add this board to list
    
    return moves    #return the list of all board




