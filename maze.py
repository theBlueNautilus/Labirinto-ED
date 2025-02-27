import pygame
import numpy as np
import csv
import random
import threading
import time  # importado para permitir delays durante a busca

class Maze:

    '''
    O labirinto é representado por uma matriz binária em arquivo. Onde
    o valor 0 representa um quadrado da parede do labirinto, e o valor 1 representa 
    um quadrado do corredor do labirinto.
    
    O labirinto em memória é representado por uma matriz inteira, indicando para cada
    quadrado se o mesmo é uma parede, um corredor, o prêmio ou o jogador.
    '''
    
    WALL = 0
    HALL = 1
    PLAYER = 2
    PRIZE = 3
    
    def __init__(self):
        '''
        Inicializa a matriz de inteiros M que representa a lógica do labirinto
        '''
        self.M = None  # matriz que representa o labirinto
        pygame.init()

    def load_from_csv(self, file_path : str):
        '''
        Função para carregar a matriz de um arquivo CSV  
        Parameters
        ----------
        file_path : str
            Nome do arquivo contendo a matriz binária que descreve o labirinto.
        '''
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.M = np.array([list(map(int, row)) for row in reader])
            
    def init_player(self):
        '''
        Coloca o prêmio (quadrado amarelo) e o jogador (quadrado azul)
        em posições aleatórias no corredor do labirinto.
        '''
        # Escolhendo a posição aleatória do player em um corredor
        while True:
            posx = random.randint(2, self.M.shape[0]-2)
            posy = random.randint(2, self.M.shape[1]-2)
            if self.M[posx, posy] == Maze.HALL:
                self.init_pos_player = (posx, posy)
                break
        
        # Escolhendo a posição aleatória do prêmio em um corredor
        while True:
            posx = random.randint(2, self.M.shape[0]-2)
            posy = random.randint(2, self.M.shape[1]-2)
            if self.M[posx, posy] == Maze.HALL and (posx, posy) != self.init_pos_player:
                self.M[posx, posy] = Maze.PRIZE
                break

    def find_prize(self, pos : (int, int)) -> bool:
        '''
        Recebe uma posição (x,y) do tabuleiro e indica se o prêmio está contido
        naquela posição.
        Parameters
        ----------
        pos : (int, int)
            Posição do quadrado na matriz do labirinto que se deseja testar se 
            foi encontrado prêmio
        Returns
        -------
        bool
            Retorna True se o quadrado do labirinto na posição 'pos' contiver o prêmio, 
            retorna False caso contrário.
        '''
        return self.M[pos[0], pos[1]] == Maze.PRIZE
        
    def is_free(self, pos : (int, int)) -> bool:
        '''
        Indica se a posição fornecida está livre para o jogador acessar, ou seja, 
        se for corredor ou prêmio.
        Parameters
        ----------
        pos : (int, int)
            Posição do quadrado na matriz do labirinto que se deseja testar se 
            está livre.
        Returns
        -------
        bool
            Retorna True se a posição for HALL ou PRIZE.
        '''
        return self.M[pos[0], pos[1]] in [Maze.HALL, Maze.PRIZE]
        
    def mov_player(self, pos : (int, int)) -> None:
        '''
        Move o jogador para uma nova posição do labirinto, atualizando a matriz.
        Parameters
        ----------
        pos : (int, int)
            Nova posição (x,y) no labirinto em que o jogador será movido.
        '''
        # Se a posição for corredor ou prêmio, marca com PLAYER.
        if self.M[pos[0], pos[1]] in [Maze.HALL, Maze.PRIZE]:
            self.M[pos[0], pos[1]] = Maze.PLAYER
        
    def get_init_pos_player(self) -> (int, int):
        '''
        Indica a posição inicial do jogador dentro do labirinto que foi gerada 
        de forma aleatória.
        Returns
        -------
        (int, int)
            Posição inicial (x,y) do jogador no labirinto.
        '''
        return self.init_pos_player
            
    def run(self):
        '''
        Thread responsável pela atualização da visualização do labirinto.
        '''
        th = threading.Thread(target=self._display)
        th.start()
    
    def _display(self, cell_size=15):
        '''
        Método privado para exibir o labirinto na tela, mapeando os valores lógicos
        atribuídos em cada casa da matriz M, conforme as constantes definidas.
        '''
        rows, cols = self.M.shape
        width, height = cols * cell_size, rows * cell_size
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Labirinto")
    
        # Cores
        BLACK = (0, 0, 0)
        GRAY = (192, 192, 192)
        BLUE = (0, 0, 255)
        GOLD = (255, 215, 0)
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
    
            screen.fill(BLACK)
    
            # Desenhar o labirinto
            for y in range(rows):
                for x in range(cols):
                    if self.M[y, x] ==  Maze.WALL:
                        color = BLACK
                    elif self.M[y, x] == Maze.HALL:
                        color = GRAY
                    elif self.M[y, x] == Maze.PLAYER:
                        color = BLUE
                    elif self.M[y, x] == Maze.PRIZE:
                        color = GOLD
                       
                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
    
            pygame.display.flip()
            time.sleep(0.05)  # pequeno delay para reduzir a carga de processamento


    ###### Função de backtracing ######
    def solve_maze_backtracking(self) -> bool: 
        # Crie uma nova pilha
        stack = []
        # Localize a posição inicial do jogador
        start = self.get_init_pos_player()
        # Insira sua localização na pilha
        stack.append(start)
        visited = set([start])
        
        # Movimentos possíveis: cima, baixo, esquerda e direita
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Enquanto a pilha não estiver vazia
        while stack:
            # Retire uma localização (linha, coluna) da pilha
            current = stack.pop()
            
            # Se a posição tiver o prêmio no local então
            if self.find_prize(current):
                print("Tesouro encontrado em:", current)
                return True
            
            # Caso contrário, se este local não contiver o prêmio
            # Mova o jogador para este local
            self.mov_player(current)
            time.sleep(0.1)
            
            # Examine se as casas adjacentes estão livres
            for move in moves:
                next_pos = (current[0] + move[0], current[1] + move[1])
                if 0 <= next_pos[0] < self.M.shape[0] and 0 <= next_pos[1] < self.M.shape[1]:
                    # Se sim insira sua posição na pilha
                    if next_pos not in visited and self.is_free(next_pos):
                        stack.append(next_pos)
                        visited.add(next_pos)
                        
        print("Caminho não encontrado!")
        return False
