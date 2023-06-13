import pygame
from .const import BLACK,WHITE,SQUARESIZE,RADI,CROWN
class Piece:
    
    def __init__(self,row,col,colors) :
        self.row = row
        self.col = col
        self.colors = colors
        self.king = False
        self.x =0
        self.y =0
        self.calculation_pos()
    
    def calculation_pos(self):
        self.x = SQUARESIZE*self.col+SQUARESIZE//2
        self.y = SQUARESIZE*self.row+SQUARESIZE//2
    
    def make_king(self):
        self.king = True

    def draw_piece(self,win):
        pygame.draw.circle(win, self.colors,(self.x,self.y),RADI)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def movement(self,row,col):
        self.row = row
        self.col = col
        self.calculation_pos()
    
    def __repr__(self):
        return str(self.colors)