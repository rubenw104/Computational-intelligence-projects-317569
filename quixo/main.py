import random
from game import Game, Move, Player
from functions import  minimax
from tqdm import tqdm
import numpy as np
class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name="RandomPlayer"
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
           
        return from_pos, move


class MyPlayer(Player):
    def __init__(self, simmetry=False) -> None:
        super().__init__()
        self.number_of_nodes=np.array([])
        self.simmetry=simmetry
        self.name="MyPlayer"
    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        
        result=minimax(game, 2, game.get_current_player(),counter_nodes=0, simmetry=self.simmetry)
        eval, (from_pos,move),counter_nodes = result
        self.number_of_nodes=np.append(self.number_of_nodes, counter_nodes)

        return from_pos, move

def play_games(number_of_games:int , verbose:bool, player1:Player, player2:Player):
    winners=[0,0]
    for _ in tqdm(range(number_of_games)):
        g = Game(verbose=verbose)
        winner = g.play(player1, player2)
        winners[winner]+=1
        g=None
    print(f'player1: {player1.name} player2: {player2.name}')
    print(f'Average of explored nodes with simmetry= {player1.simmetry if isinstance(player1, MyPlayer) else player2.simmetry}: {np.mean(player1.number_of_nodes if isinstance(player1, MyPlayer) else player2.number_of_nodes)}')
    print(f'Player 0 has won {winners[0]} games, Player 1 has won {winners[1]} games. total games: {number_of_games} ')

if __name__ == '__main__':
    
    play_games(20, verbose=True, player1=RandomPlayer(), player2=MyPlayer(simmetry=False))
