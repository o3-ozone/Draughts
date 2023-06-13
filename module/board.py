import pygame
from module.const import BROWN,LIGHTBROWN,BLACK,WHITE,ROWS,SQUARESIZE,COLS,GREY
from module.piece import Piece
class board:

    def __init__(self):
        self.board=[]
        self.black_piece = self.white_piece = 20
        self.black_king = self.white_king = 0
        self.create_board()
    
    def draws_board(self, win):
        win.fill(BROWN)
        for rows in range(ROWS):
            for col in range(rows%2,ROWS,2):
                pygame.draw.rect(win,LIGHTBROWN,(rows*SQUARESIZE,col*SQUARESIZE,SQUARESIZE,SQUARESIZE))
                
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (col + row) % 2 >0:
                    if row<4:
                        self.board[row].append(Piece(row,col,BLACK))
                    elif row>5:
                        self.board[row].append(Piece(row,col,WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_all(self,win):
        self.draws_board(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 :
                    piece.draw_piece(win)
    
    def movement(self,piece,row,col):
        self.board[piece.row][piece.col] ,self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        piece.movement(row,col)
        if row == ROWS-1:
            if piece.colors == BLACK:
                piece.make_king()
                self.black_king +=1
        elif row == 0:
            if piece.colors == WHITE:
                piece.make_king()
                self.white_king +=1

    def get_piece(self,row,col):
        return self.board[row][col]
    
    def mid_game_evaluate(self):
        return self.black_piece*2 - self.white_piece*2 + (self.black_king*0.5- self.white_king*0.5)
    def evaluate(self):
        return self.black_piece - self.white_piece + (self.black_king*0.5- self.white_king*0.5)
    def end_game_evaluate(self):
        return self.black_piece*0.5 - self.white_piece*0.5 + (self.black_king- self.white_king)

    def get_all_piece(self,color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece!=0 and piece.colors == color:
                    pieces.append(piece)
        return pieces

    def get_avalible_move(self,piece):
        moves = {}
        left = piece.col -1
        right = piece.col+1
        row = piece.row
        if piece.colors == BLACK :
            moves.update(self._move_left_up(row+1,min(row+3,ROWS),1,piece.colors,left))
            moves.update(self._move_right_up(row+1,min(row+3,ROWS),1,piece.colors,right))
            if row > 1 :
                moves.update(self._move_left_jump(row-1,max(row-3,-1),-1,piece.colors,left))
                moves.update(self._move_right_jump(row-1,max(row-3,-1),-1,piece.colors,right))
          
        if piece.king :
            moves.update(self._move_king_left(row+1,min(row+10,ROWS),1,piece.colors,left))
            moves.update(self._move_king_right(row+1,min(row+10,ROWS),1,piece.colors,right))
            moves.update(self._move_king_right(row-1,max(row-10,-1),-1,piece.colors,right))
            moves.update(self._move_king_left(row-1,max(row-10,-1),-1,piece.colors,left))

        if piece.colors == WHITE :
            moves.update(self._move_left_up(row-1,max(row-3,-1),-1,piece.colors,left))
            moves.update(self._move_right_up(row-1,max(row-3,-1),-1,piece.colors,right))
            if row <8:
                moves.update(self._move_left_jump(row+1,max(row+3,ROWS),1,piece.colors,left))
                moves.update(self._move_right_jump(row+1,max(row+3,ROWS),1,piece.colors,right))
    

        return moves
    
    def _move_left_up(self,start,stop,step,color,left,skip = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skip and not last:
                    break
                elif skip:
                    moves[(r, left)] = last + skip
                else:
                    moves[(r, left)] = last
                break
            elif current.colors == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves
    
    def _move_right_up(self,start,stop,step,color,right,skip = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skip and not last:
                    break
                elif skip:
                    moves[(r,right)] = last + skip
                    
                else:
                    moves[(r, right)] = last
                
                break
            elif current.colors == color:
                break
            else:
                last = [current]

            right += 1
        return moves
    
    def _move_king_left(self,start,stop,step,color,left,skip = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skip and not last:
                    break
                if last:
                    moves[(r,left)] = last
                    break
                elif skip:
                    moves[(r,left)] = last + skip
                moves[(r, left)] = last

            elif current.colors == color:
                break
            else:
                if last:
                    break
                last = [current]

            left -= 1
        return moves
    
    def _move_king_right(self,start,stop,step,color,right,skip = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skip and not last:
                    break
                if last:
                    moves[(r,right)] = last
                    break
                else:
                    moves[(r, right)] = last

            elif current.colors == color:
                break
            
            else:
                if last:
                    break
                last = [current]

            right += 1
        return moves

    def _move_left_jump(self, start, stop, step, color, left, skip=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skip and not last:
                    break
                if last:
                    moves[(r, left)] = last 
                    break
                
            elif current.colors == color:
                break
            else:
                last = [current]
                left -= 1
        return moves

    def _move_right_jump(self,start,stop,step,color,right,skip = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right > COLS-1:
                break
            current = self.board[r][right]
            if current == 0:
                if skip and not last:
                    break
                if last:
                    moves[(r, right)] = last 
                    break
                
            elif current.colors == color:
                break
            else:
                last = [current]
                right += 1
        return moves
       
    def remove(self, piece):
        for pieces in piece:
            self.board[pieces.row][pieces.col] = 0
            if pieces != 0:
                if pieces.colors == BLACK:
                    self.black_piece -= 1
                else:
                    self.white_piece -= 1

    def winner(self):
        if self.white_piece <= 0:
            return WHITE
        elif self.black_piece <= 0:
            return BLACK
        return None 