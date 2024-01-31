from game import Game, Move
from copy import deepcopy, copy
from random import choice
import numpy as np

perimeter={(0,0), (1,0), (2,0), (3,0), (4,0),
               (0,1),                      (4,1),
               (0,2),                      (4,2),
               (0,3),                      (4,3),
               (0,4), (1,4), (2,4), (3,4), (4,4)}

def acceptable_move(game:Game,from_pos: tuple[int, int], slide: Move, player_id):
    """given a move(from_pos + slide) and a player, tells if it is acceptable"""
    old_r=old_row(game,from_pos,slide)
    acceptable: bool =game._Game__move(from_pos, slide, player_id)
    if acceptable:
        undo_move(game,from_pos,slide,old_r)
    return acceptable

def score(game: Game, player_id, depth):
    """Calculates scores player_id's perspective """
    
    opponent= (player_id +1)%2
    if game.check_winner() ==player_id:
        #a win with few steps is more valuable
        return 1000 + depth
    elif game.check_winner()== opponent:
        #a lose with many steps is less valuable
        return -1000 - depth
    else:
        #instead of returning 0, I give preference to nodes less deep
        return depth

def is_symmetric(board1, board2) ->bool:
    return (np.array_equal(board1, board2) or np.array_equal(np.rot90(board1), board2) 
            or np.array_equal(np.rot90(board1, 2), board2) or np.array_equal(np.rot90(board1, 3), board2) 
            or np.array_equal(np.flip(board1, axis=1), board2) or np.array_equal(np.flip(board1, axis=0), board2)
            or np.array_equal(np.rot90(np.flip(board1, axis=1)), board2)
            or np.array_equal(np.rot90(np.flip(board1, axis=1),3), board2) )

def available_moves(game: Game, player_id: int, simmetry:bool =True, perimeter=perimeter)->set:
    """returns list of possible moves (move, slide)"""
    board= game._board
    availables=set()
    for move in perimeter:
        if board[(move[1], move[0])]==player_id or board[(move[1], move[0])]==-1:
            for slide in Move:
                if acceptable_move(game, move, slide, player_id):
                    if simmetry:
                        # move,slide is acceptable-> find the relative board->
                        # find symmetrical boards -> check if they are already inside availables
                        
                        #retrieve board after move
                        old_r1=old_row(game, move, slide)        
                        game._Game__move( move, slide, player_id)
                        board_1=copy(game._board)
                        undo_move( game,move, slide, old_r1)
                        
                        simmetrycal=False
                        for available in availables:
                            #retrieve board
                            old_r2=old_row(game, available[0], available[1])        
                            game._Game__move( available[0], available[1], player_id)
                            
                            #checks if there is already a symmetric move
                            if is_symmetric(board_1, game._board):
                                simmetrycal=True

                            
                            undo_move( game,available[0], available[1], old_r2)
                        if simmetrycal == False:
                            availables.add((move,slide))
                    else: 
                        availables.add((move,slide))
    return availables

def game_over(game: Game)-> bool:
    """returns True if game is over"""
    if game.check_winner()==1 or game.check_winner()==0:
        return True
    else:
        return False

def undo_move(game:Game, move:tuple, slide: Move, old_r):
    """function that undoes the move in input"""
    if slide== Move.RIGHT or slide== Move.LEFT:
        game._board[move[1],:]=deepcopy(old_r)
    else:
        game._board[:,move[0]]=deepcopy(old_r)
    return move

def old_row(game:Game, move:tuple, slide: Move):
    """function that returns the old row or column before a move"""
    if slide== Move.RIGHT or slide== Move.LEFT:
        return deepcopy(game._board[move[1],:])
    else:
        return deepcopy(game._board[:,move[0]])


def minimax(game:Game, depth:int, player_id:int, is_maximizing_player:bool=True, alfa:float=float('-inf'), beta:float= float('inf'), counter_nodes=0, simmetry=True):
    """returns the evaluation of the chosen node, the move associated and the number of explored nodes"""
    counter_nodes+=1
    if depth<=0 or game_over(game)==True:
        return score(game, player_id, depth), None, counter_nodes
        

    if is_maximizing_player and game_over(game)==False:
        max_eval = float('-inf')
        best_move = None
        availables=available_moves(game, player_id, simmetry)
        for (move,slide) in availables:
            #g=deepcopy(game)
            old_r=old_row(game, move, slide)
            
            #g._Game__move( move, slide, player_id)
            game._Game__move( move, slide, player_id)
            #eval,_ = minimax2(g, depth - 1,player_id, False,alfa,beta)
            eval,_, counter_nodes = minimax(game, depth - 1,player_id, False,alfa,beta, counter_nodes)
            undo_move(game, move,slide, old_r)

            if eval > max_eval:
                max_eval = eval
                best_move = (move,slide)
            if max_eval > alfa:
                alfa = max_eval
            #g=None
            if beta<=alfa :
                break
        return max_eval, best_move,counter_nodes
    elif game_over(game)==False:
        min_eval = float('inf')
        best_move = None
        availables=available_moves(game, (player_id+1)%2, simmetry)
        for (move,slide) in availables:
            #g=deepcopy(game)
            old_r=old_row(game, move, slide)

            #g._Game__move( move, slide, (player_id+1)%2)
            game._Game__move( move, slide, (player_id+1)%2)
            #eval, _ = minimax2(g, depth - 1, player_id, True, alfa, beta)
            eval, _,counter_nodes = minimax(game, depth - 1, player_id, True, alfa, beta, counter_nodes)
            undo_move(game, move,slide, old_r)
            if eval < min_eval:
                min_eval = eval
                best_move = (move,slide)
            #g=None
            if min_eval< beta:
                beta=min_eval

            if beta <=alfa :
                break
        return min_eval, best_move,counter_nodes