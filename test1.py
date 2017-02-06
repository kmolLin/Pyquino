from pazudorasolver.board import Board
from pazudorasolver.piece import Fire, Wood, Water, Dark, Light, Heart, Poison, Jammer, Unknown
from pazudorasolver.heuristics.greedy_dfs import GreedyDfs
from pazudorasolver.heuristics.pruned_bfs import PrunedBfs

weights = {Fire.symbol: 2.0,
           Wood.symbol: 2.0,
           Water.symbol: 2.0,
           Dark.symbol: 2.0,
           Light.symbol: 2.0,
           Heart.symbol: 1.0,
           Poison.symbol: 0.5,
           Jammer.symbol: 0.5,
           Unknown.symbol: 0.0}

#board = Board.create_randomized_board(5, 6)


piece_list = [Fire,  Wood,  Water, Dark,  Light, Heart,
              Fire,  Water, Dark,  Light, Heart, Fire,
              Fire,  Water, Dark,  Heart, Heart, Wood,
              Light, Water, Light, Fire,  Wood,  Wood,
              Dark,  Water, Dark,  Light, Light, Light]
number_of_rows = 5
number_of_columns = 6
board = Board(piece_list, number_of_rows, number_of_columns)
matches = board.get_matches()

print (board)
print (matches)


solver1 = GreedyDfs(weights)
solution = solver1.solve(board, 100)

print (solution)

solver2 = PrunedBfs(weights)
solution = solver2.solve(board, 100)

print (solution)
