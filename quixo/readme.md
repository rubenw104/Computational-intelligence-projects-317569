I started with the idea of using minimax, because it fits well with the game of Quixo, that is turn 
based, zero sum, deterministic and with perfect information. The simple-”naive” minimax was too 
slow because, given the structure of the Quixo game, there are too many possible moves and 
consequently too many nodes to explore in the game tree. 

First improvement: I had to pass a parameter that takes into account the maximum depth reached by 
the tree, and I did this through a variable called 'depth.' 

Second improvement: "depth” alone was not sufficient, and, of course, I had to add alpha-beta 
pruning, which allowed me to avoid exploring quite a few nodes. 

Third improvement: Another modification I made was to remove all calls to the deepcopy function 
for the game class to speed up the code. In particular, the possible move is applied to the actual 
game instance and then undone through a custom function called 'undo()'. To do this, it was 
necessary to retain the content of the row of the board to which the move is applied. For this 
purpose, I created the function 'old_row()'.

Fourth improvement: Finally, to further reduce the nodes to visit, I modified the 'available_moves' 
function to return only one among the possible symmetric moves. It is done if the “simmetry” 
parameter is set to True when calling minimax. In the screenshots, you can see the difference 
in terms of the average number of nodes visited per call to the minimax function between cases with 
simmetry=True and simmetry=False. 

Fifth improvement: I also tried to use numpy arrays or sets in order to maximize the speed of the 
code.

Although a precise estimate is challenging, the algorithm's results are more than satisfactory.
Talking about the symmetry, I found very helpful this essay: https://arxiv.org/pdf/2007.15895.pdf
. In fact, it helped me in the base idea behind the development of the is_symmetric() function.