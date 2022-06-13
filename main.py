
import pygame
from checkers.game import Game
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED ,WHITE
from Algo.algorithm import minimax

FPS = 60   #time of wait
    #window design
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #width and height of window
pygame.display.set_caption('Checkers')      #name of window

def get_row_col_from_mouse(pos):    #where mouse click
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock() #define clock
    # board = Board()             #object from calss Board  #deleted because the line below (Game) initial make object from Board
    game = Game(WIN)    #instade of the above line

    # pec=board.get_piece(0, 1)  for check only
    # board.move(pec, 7, 3)      for check only


    #event loop
    while run:
        clock.tick(FPS) #wait

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.ai_move(new_board)

#
        if game.winner() != None:   #if exist winner
            print(game.winner())
            run = False             #exist loop
#
        for event in pygame.event.get():    #loop for get event from user
            if event.type == pygame.QUIT:   #if user pressure on X
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:    #condition when click mouse
                pos = pygame.mouse.get_pos()            #read position of click
                row, col = get_row_col_from_mouse(pos)  #send the position to function to get the row and clomns of click
                game.select(row, col)

                # pec = board.get_piece(row, col) #for check only
                # board.move(pec, 7, 3)      #for check only



        # board.draw(WIN) #drow the fill board
        # pygame.display.update() #display the change of board
#
        game.update()   #we call the function instade of the above two lines
#
    pygame.quit()   #exit window
#
main()