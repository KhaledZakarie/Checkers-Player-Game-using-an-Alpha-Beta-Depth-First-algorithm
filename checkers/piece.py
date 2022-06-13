from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame
#
class Piece:
    PADDING = 15   #size of circle piece
    OUTLINE = 2     #outline of circle
#
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color  #the color of stand pieces
        self.king = False
        self.x = 0  #firt piece
        self.y = 0  #second piece
        self.calc_pos() #call in evey init to mack the piece in the middel of square
#
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2  #to stand the first piece in center of square
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2  #to stand the first piece in center of square
#
    def make_king(self):    #to chenge piece to king
        self.king = True
#
    def draw(self, win):    #to draw the circle of piece
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:   #put the crown in piece
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))
#

    def move(self, row, col): #done the move
        self.row = row
        self.col = col
        self.calc_pos()
