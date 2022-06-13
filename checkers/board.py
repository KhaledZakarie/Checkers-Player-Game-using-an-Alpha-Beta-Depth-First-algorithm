import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece
#
class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12    #num of red and white squares
        self.red_kings = self.white_kings = 0   #num of kings in each color
        self.create_board()                     #to initial stand in the board

    def draw_squares(self, win):
        win.fill(BLACK)     #fill the board with black
        for row in range(ROWS):     #loop in each row
            for col in range(row % 2, COLS, 2): #loop in one clomns and skep next
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))   #drow the red
#
    def move(self, piece, row, col):    #where the piece will move
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] #swap the design
        #the (piece.row)the old place of piece = (row) the new row  that user will move the piece to
        piece.move(row, col)    #call the function in class piece that move and calc position of piece

        if row == ROWS - 1 or row == 0: #if the row that the piece will move to ,is the final r0w(7) or is first row(0)
            piece.make_king()           #make the piece is king
            if piece.color == WHITE:
                self.white_kings += 1   #increment num of kings of white
            else:
                self.red_kings += 1     #increment num of kings of red
#
    def get_piece(self, row, col):
        return self.board[row][col]
#
    def create_board(self): #create the actual internal representation of board with pieces
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2): #condition of where the piece stand
                    if row < 3:     #0,1 and 2 is the place of white piece
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:   #5,6 and 7 is the place of red piece
                        self.board[row].append(Piece(row, col, RED))
                    else:   #if 3 and 4 is empty place
                        self.board[row].append(0)
                else:                            #where no stand piece
                    self.board[row].append(0)
#
    def draw(self, win):    #draw the pieces
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
#
    def remove(self, pieces):   #pieces is the dictionary of skipped dictionary
        for piece in pieces:    #loop i skipped
            self.board[piece.row][piece.col] = 0    #replace the piece by 0
            if piece != 0:                  #if the piece is't 0 (is piece)
                if piece.color == RED:
                    self.red_left -= 1      #dicrese the num of pieces
                else:
                    self.white_left -= 1    #dicrese the num of pieces

    def winner(self):   #the winer
        if self.red_left <= 0:  #if num pieces of red is 0 (no exit red piece)
            return WHITE        #return the white
        elif self.white_left <= 0:  #if num pieces of white is 0 (no exit white piece)
            return RED              #return the red

        return None     #if exist red and white pieses
#
    def get_valid_moves(self, piece):   #return the valid move of this piece
        moves = {}  #move : skiped
        left = piece.col - 1    #left diagnol -> mean move left in the same row -> need to down or up
        right = piece.col + 1   #right diagnol -> mean move right in the same row -> need to down or up
        row = piece.row         #row = the row that the piece is stand

        if piece.color == RED or piece.king:    #if this piece is red or is king   -> will move up,king mean if king will move up and down
            #add in move
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))    #start look from row-1 and looking until row -2 or be in row -1
            #send to method->the above row of piece, loop 2 row if untill find row 0 , step is one for up, color, col before the piece
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))  #start look from row-1 and looking until row -2 or be in row -1
        if piece.color == WHITE or piece.king:  #if this piece is white or is king   -> will move down
            #add in move
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))   #start look from row+1 and looking until row +2 or be in the last row(7)
            # send to method->the under row of piece, loop 2 row if untill find row 7 , step is one for , color, col before the piece
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right)) #start look from row+1 and looking until row +2 or be in the last row(7)

        return moves    #return the valid move
#
    def _traverse_left(self, start, stop, step, color, left, skipped=[]): #stat,stop,step->rows , left -> col
        #start=the abouve or under of piece, the 2row up or down of piece,step,color,before of piece, list of piece i juped over them
        moves = {}  #the valid move
        last = []   #place of aginest piece
        for r in range(start, stop, step):    #loop in rows->the 2row up or down of piece
            if left < 0:      #if we outside the board
                break         #exit loop

            current = self.board[r][left]   #the first diagonal in left of piece
            if current == 0:    #if the current place is zero (empty place//can stand on)
                if skipped and not last:    #skipped mean i jumped on aginest piece, not last mean the diagonal not agienest piece
                    break
                elif skipped:   #jumped over piece && the diagoal is agienest piece
                    moves[(r, left)] = last + skipped   #put on valid list of this piece the place of jumped piece and diagonal piece
                else:           #not jumped over any piece
                    moves[(r, left)] = last #put on valid move the diagonal

                if last:        #if is agienest piece in diagonal place
                    if step == -1:      #if i up
                        row = max(r-3, 0)   #make the row up 2row
                    else:               #if i down
                        row = min(r+3, ROWS)    #make the row down 2row
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last)) #call agien this method with up or down 2row and put the diagonal piece in skipped
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:    #if in this place exist the same color of piece (same player)
                break
            else:   #if in current found agienst piece (diffe color)
                last = [current]    #last = the current -> = the agenist player

            left -= 1   # move to the col before to check the diagnal

        return moves
#
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    ###############################################AI###################################################

    def evaluate(self): #tell us the score (postive number or negative number tell us the score of this board)
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):    #get all pieces of this color
        pieces = [] #list of pieces without zero place
        for row in self.board:  #loop in rows
            for piece in row:   #loop in col
                if piece != 0 and piece.color == color: #if the piece is the my clolr piece
                    pieces.append(piece)    #add the piece to list of pieces
        return pieces