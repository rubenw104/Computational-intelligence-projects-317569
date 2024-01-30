import random
from game import Game, Move, Player
from copy import deepcopy
from pprint import pprint
from functions import acceptable_move,available_moves,score, minimax,update_player_id, game_over,minimax2, old_row, undo_move
from random import choice
from tqdm import tqdm
import numpy as np
class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        # if game.verbose:
        #     print("Actual board")
        #     game.print()
        #     print(f'Player {game.get_current_player()} does: {from_pos}  MOVE: {move}')
            
        return from_pos, move


class MyPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
    
    
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # from_pos = (random.randint(0, 4), random.randint(0, 4))
        # move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        # try:
        result=minimax2(game, 2, game.get_current_player(),counter_nodes=0)
        eval, (from_pos,move),counter_nodes = result
            #print(counter_nodes)
        # except TypeError:
        #     print("There was an error in minmax, a random move has been taken")
        #     from_pos = (random.randint(0, 4), random.randint(0, 4))
        #     move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

def play_games(number_of_games:int , verbose:bool, player1:Player, player2:Player):
    winners=[0,0]
    for _ in tqdm(range(number_of_games)):
        g = Game(verbose=verbose)
        winner = g.play(player1, player2)
        winners[winner]+=1
        # g.print()
        # print(f"Winner: Player {winner}")
        g=None
    
    print(f'Player 0 has won {winners[0]} games, Player 1 has won {winners[1]} games. total games: {number_of_games} ')

if __name__ == '__main__':
    # g = Game(verbose=True)
    # g.print()
    # player1 = MyPlayer()
    # player2 = RandomPlayer()
    # winner = g.play(player1, player2)
    # g.print()
    # print(f"Winner: Player {winner}")

    # print("actual game: ",g._board, sep="\n")
    # #conserva la vecchia riga
    # mossa=(0,2), Move.RIGHT
    # old_r=old_row(g,mossa[0], mossa[1])
    # print("old row ", old_r, sep=" ")
    # #fai la mossa
    # g._Game__move(*mossa,0)
    # print("game after move: ",g._board, sep="\n")
    # #annulla la mossa
    # undo_move(g,mossa[0], mossa[1],old_r)
    # print("game after undo: ",g._board, sep="\n")

    play_games(100, verbose=False, player1=MyPlayer(), player2=RandomPlayer())
    play_games(100, verbose=False, player1=RandomPlayer(), player2=MyPlayer())
    # g=Game(verbose=False)
    # move=(0,0)
    # g._Game__move((0,4),Move.TOP,-1)
    # pprint(g._board)
    # g= Game(verbose=True)
    # g.print()
    # current_player=0
    # for _ in range(20):
    #     move,slide=choice(available_moves(g,current_player))
    #     g._Game__move(move,slide, current_player)
    #     print(f"Move number:{_}, Player: {current_player}, Move:{move}, Slide: {slide}")
    #     g.print()
    #     current_player=update_player_id(current_player)
    #     if game_over(g):
    #         break
    
    # eval, (move,slide) = minimax2(deepcopy(g), 4, True)
    # print(move,slide,eval, sep=" ")
    # g=Game(verbose=True)
    # print(available_moves(g,0))