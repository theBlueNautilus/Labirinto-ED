# -*- coding: utf-8 -*-
import time
from maze import Maze
from collections import deque

s = deque()


maze_csv_path = "labirinto1.txt" #Insira aqui o caminho do diretório para o labirinto1.txt
maze = Maze() 

maze.load_from_csv(maze_csv_path)

# Exibir o lab
maze.run()
maze.init_player()
maze.solve_maze_backtracking()



