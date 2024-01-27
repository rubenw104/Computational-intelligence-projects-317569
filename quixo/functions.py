from game import Game, Move
from copy import deepcopy
from random import choice
# import sys
# sys.setrecursionlimit(sys.getrecursionlimit()*10)

def acceptable_move(game:Game,from_pos: tuple[int, int], slide: Move, player_id):
    """given a move(from_pos + slide) and a player, tells if it is acceptable"""
    g= deepcopy(game)
    acceptable: bool =g._Game__move(from_pos, slide, player_id)
    return acceptable

def score(game: Game, player_id, depth):
    """Calculates scores from X's perspective """
    
    opponent=update_player_id(player_id)
    if game.check_winner() ==player_id:
        return 10 + depth
    elif game.check_winner()== opponent:
        return -10 - depth
    else:
        return 0

def available_moves(game: Game, player_id: int):
    """returns list of possible moves (move, slide)"""
    board= game.get_board()
    availables=list()
    perimeter=[(0,0), (1,0), (2,0), (3,0), (4,0),
               (0,1),                      (4,1),
               (0,2),                      (4,2),
               (0,3),                      (4,3),
               (0,4), (1,4), (2,4), (3,4), (4,4)]
    for move in perimeter:
        #first and last column
        if board[(move[0], move[1])]==player_id or board[(move[0], move[1])]==-1:
            for slide in Move:
                if acceptable_move(game, move, slide, player_id):
                    availables.append((move,slide))
    return availables

def game_over(game: Game)-> bool:
    """returns True if game is over"""
    if game.check_winner()==1 or game.check_winner()==0:
        return True
    else:
        return False

def update_player_id(current_player)-> int:
    if current_player==0:
        return 1
    elif current_player==1:
        return 0
    else:
        return None

def minimax(game: Game, player_id):
    if game_over(game):
        return score(game, player_id)
    
    current_player= player_id
    scores = [] # an array of scores
    moves = []  # an array of moves

    if len(available_moves(game, current_player))==0:
        return 0
    for (move,slide) in available_moves(game, current_player):
        g= deepcopy(game)
        #makes one of the possible moves
        possible_game = g._Game__move( move, slide, current_player)
        assert possible_game== True, "Mossa non valida"
        #changes current player
        current_player= update_player_id(current_player)
        #calculates scores by recursion until game_over
        scores.append(minimax(g, current_player))
        moves.append((move,slide))
    
    return moves,scores

def minimax2(game:Game, depth:int, is_maximizing_player:bool):
    if depth<=0 or game_over(game)==True:
        return score(game, 0, depth), None
        

    if is_maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for (move,slide) in available_moves(game, 0):
            g=deepcopy(game)
            g._Game__move( move, slide, 0)
            eval,_ = minimax2(g, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = (move,slide)
            g=None
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for (move,slide) in available_moves(game, 1):
            g=deepcopy(game)
            g._Game__move( move, slide, 1)
            eval, _ = minimax2(g, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = (move,slide)
            g=None
        return min_eval, best_move