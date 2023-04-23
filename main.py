import pygame
from module import WIDTH,HEIGHT,SQUARESIZE,board,BLACK,WHITE
from module.game import Game
from module.piece import piece

FPS=60
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Draughts")

def get_pos_from_mouse(pos):
    x,y = pos
    row= y//SQUARESIZE
    col=x//SQUARESIZE
    return row,col

def main():
    run = True
    clock = pygame.time.Clock()
    games = Game(WIN)
    while run:
        clock.tick(FPS)
        
        if games.winner() != None:
            print(games.winner())

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False
            if events.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(games.turn)
                if games.turn == WHITE:
                        row , col = get_pos_from_mouse(pos)
                        games.select(WHITE,row,col)

                if games.turn == BLACK:
                        row , col = get_pos_from_mouse(pos)
                        games.select(BLACK,row,col)

        games.update()

    pygame.quit()
    
main()