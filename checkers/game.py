import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board
#
class Game:
    def __init__(self, win):
        self._init()    #call the function initial the attrbute
        self.win = win  #to select the window we will play in because if we playing many play
#
    def update(self):     #to draw every update istade of draw every time such draw in main in the first draw of board
        self.board.draw(self.win)   #drow the fill board
        self.draw_valid_moves(self.valid_moves) #drow valid moves
        pygame.display.update()     #display the change of board

#
    def _init(self):            #initialization
        self.selected = None
        self.board = Board()    #object from Board
        self.turn = RED         #the red is turn to play
        self.valid_moves = {}   #it for tell us what the valid move allow for you

    def winner(self):
        return self.board.winner()
#
    def reset(self):       #play from first
        self._init()
#
    def select(self, row, col):     #the selected piece -- the row and col i selected
        if self.selected:   #if we allready selected piece ->mean i allready have a piece and this row,col are which i want to move to
            result = self._move(row, col)   #try to move it to row,col
            if not result:      #if we can't move (found piece in this place)
                self.selected = None    #reset the selected to none
                self.select(row, col)   #then recall this method with the row,col ->mean i don't selected before and this row,col is the piece i selected to put them in selected var

        piece = self.board.get_piece(row, col)      #get the piece of the raw and col that I selected to put it in selected var
        if piece != 0 and piece.color == self.turn: #if the place that I enter row and col of them is piece(not zero) and the piece in this place is my piece
            self.selected = piece   #put this row,col (piece) in selected var
            self.valid_moves = self.board.get_valid_moves(piece)    #get the vaild move can this piece move to
            return True   # selected piece is done

        return False    #don't selected piece -> if we move piece it will return false because i don't selected piece ,i selected before
#
    def _move(self, row, col):  #check can move the piece or not ,if can then move
        piece = self.board.get_piece(row, col)      #get the piece of this row and col
        if self.selected and piece == 0 and (row, col) in self.valid_moves: #if selected piece(not zero) and the row,col I will move to is in valid move of this piece
            self.board.move(self.selected, row, col)    #done the move
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)  #delected blue crecle
            self.change_turn()      #after move change the player
        else:                   #if the place is not empty or isn't valid move for this piece
            return False    #don't moved

        return True     #move is done
#
    def draw_valid_moves(self, moves): #moves is dictionary
        for move in moves:  #loop in dictionart
            row, col = move #row,col = the key of dictionart
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)    #drow circle in middle square
#
    def change_turn(self): #change the player
        self.valid_moves = {}   #before change the player (after move piece) will reset the valid move this piece
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

   ###############################################AI###################################################

    def get_board(self):
        return self.board

    def ai_move(self, board):   #to Guess the moves
        self.board = board
        self.change_turn()