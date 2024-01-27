import random
from game import Game, Move, Player
from copy import deepcopy
from pprint import pprint
from functions import acceptable_move,available_moves,score, minimax,update_player_id, game_over,minimax2
from random import choice
from tqdm import tqdm

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
        self.errors=0
    
    
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        # from_pos = (random.randint(0, 4), random.randint(0, 4))
        # move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        try:
            eval, (from_pos,move) = minimax2(deepcopy(game), 3, True)
            # print(eval)
        except TypeError:
            print("There was an error in minmax, a random move has been taken")
            self.errors+=1
            from_pos = (random.randint(0, 4), random.randint(0, 4))
            move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

def play_games(number_of_games:int , verbose:bool):
    winners=[0,0]
    for _ in tqdm(range(number_of_games)):
        g = Game(verbose=verbose)
        player1 = MyPlayer()
        player2 = RandomPlayer()
        winner = g.play(player1, player2)
        winners[winner]+=1
        # g.print()
        # print(f"Winner: Player {winner}")
        g=None
    
    print(f'Player 0 has won {winners[0]} games on {number_of_games} total games')
    print(f'Number of errors: {player1.errors} ')

if __name__ == '__main__':
    # g = Game(verbose=True)
    # g.print()
    # player1 = MyPlayer()
    # player2 = RandomPlayer()
    # winner = g.play(player1, player2)
    # g.print()
    # print(f"Winner: Player {winner}")
    
    play_games(10, verbose=True)
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