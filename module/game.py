import pygame
from module.board import board
from module.const import BLACK,WHITE,GREY,SQUARESIZE,DRAW

class Game:
    
    def __init__(self,win):
        self.select_piece = None
        self.Board=board()
        self.turn = WHITE
        self.avalible_move={}
        self.win =win
    
    def update(self): 
        self.Board.draw_all(self.win)
        self.draw_avalable_move(self.avalible_move)
        pygame.display.update()
    
    def reset(self):
        self.select_piece = None
        self.Board=board()
        self.turn = WHITE
        self.avalible_move={}

    def select(self,color,row,col):
        if self.select_piece:
            result = self._move(color,row, col)
            if not result:
                self.select_piece = None
                self.select(color,row, col)
        
        piece = self.Board.get_piece(row, col)
        if piece != 0 :
            self.select_piece = piece
            self.avalible_move = self.Board.get_avalible_move(piece)
            return True
            
        return False

    def _move(self,color,row,col):
        piece =  self.Board.get_piece(row,col)
        if self.select_piece and piece == 0 and (row,col) in self.avalible_move:
            self.Board.movement(self.select_piece , row ,col)
            skipped = self.avalible_move[(row,col)]
            if color == self.turn:
                    while True:
                        if skipped:
                            self.Board.remove(skipped)
                            piece = self.Board.get_piece(row, col)
                            nextmove = self.Board.get_avalible_move(piece)
                            multi_jump_check = list(nextmove.values())
                            if multi_jump_check:
                                if len(multi_jump_check) == 1:
                                    if multi_jump_check[0] == [(0, 0, 0)]:
                                        skipped = []
                                        if skipped:
                                            self.Board.remove(skipped)
                                    else:
                                        self.turn = WHITE if self.turn == BLACK else BLACK
                                        self.select_piece = (row, col)
                                        self.avalible_move = nextmove
                                elif len(multi_jump_check) == BLACK:
                                    if multi_jump_check[0] != [[]]:
                                        self.turn = WHITE if self.turn == BLACK else BLACK
                                        self.select_piece = (row, col)
                                        self.avalible_move = nextmove
                                    elif multi_jump_check[1] != [[]]:
                                        self.turn = WHITE if self.turn == BLACK else BLACK
                                        self.select_piece = (row, col)
                                        self.avalible_move = nextmove
                                    else:
                                        self.turn = WHITE if self.turn == BLACK else BLACK
                                        self.avalible_move = {}
                                        break
                                else:
                                    self.turn = WHITE if self.turn == BLACK else BLACK
                                    self.avalible_move = {}
                                    break
                            else:
                                self.turn = WHITE if self.turn == BLACK else BLACK
                                self.avalible_move = {}
                                break
                        else:
                            self.turn = WHITE if self.turn == BLACK else BLACK
                            self.avalible_move = {}
                            break

        else:           
            return False
        
        return True


    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_avalable_move(self,moves):
        for move in moves:
            row,col=move
            pygame.draw.circle(self.win,GREY,(col*SQUARESIZE+SQUARESIZE//2, row*SQUARESIZE+SQUARESIZE//2),15)
    
    def remove(self,piece):
        for piecs in piece:
            self.Board[piecs.row][piecs.col]=0

    def winner(self):
         if self.Board.black_piece <= 0:
            return WHITE
         elif self.Board.white_piece <= 0:
            return BLACK    
         elif self.Board.white_piece==1 and self.Board.black_piece==1:
             if self.Board.white_king == self.Board.black_king:
                return DRAW
         return None 