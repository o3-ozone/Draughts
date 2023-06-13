from copy import deepcopy
import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)

def minmax(position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or position.winner() != None:
        return position.mid_game_evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        moves = get_all_moves(position, WHITE, game)
        for move in get_all_moves(position, WHITE, game):
            evaluation = minmax(move, depth-1, False, game, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        moves = get_all_moves(position, BLACK, game)
        for move in get_all_moves(position, BLACK, game):
            evaluation = minmax(move, depth-1, True, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        
        return minEval, best_move

def simulate_move(piece, move, board, game, skip):
    board.movement(piece, move[0], move[1])
    if skip:
        board.remove(skip)
        
    return board

def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_piece(color):
        valid_moves = board.get_avalible_move(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves

def draw_moves(game, board, piece):
    valid_moves = board.get_avalible_move(piece)
    board.draw_all(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_avalable_move(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(500)
