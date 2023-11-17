First of all I changed the code to make it respect the bound k of maximal items to be taken.

Then, in the "Strategies" section, I added some rules that can be used as parameters in the adaptive algorithm.

In game section there are some functions used to test the game. At the end of the days, the only one that I used in the fitness function was the one called "game2". 

Same for fitness: I tried different ones, but the one that works is the one called "fitness2".

Talking about the evolution strategy, the chosen one is the (mu+lambda). I chose percentages as parameters to optimize, each associated to one rule. It seems working 
