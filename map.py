import pygame as pg

_ = False
mini_map = [
    #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
    [9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 8, 9, 9, 9, 8, 9, 9, 9, 8, 9, 9, 9, 9, 9], # 0
    [9, _, _, _, 9, _, _, _, _, _, _, 9, _, _, _, _, _, _, _, _, _, _, _, _, 9], # 1 
    [9, _, _, _, 9, _, 9, 8, 9, 9, _, _, _, 9, _, _, _, _, 9, _, _, 8, 9, _, 8], # 2 
    [9, _, _, _, _, _, 9, _, _, _, _, 9, 8, 8, 8, 9, 9, 9, _, _, _, _, 9, _, 9], # 3 
    [9, _, _, _, 9, _, _, _, 8, 8, _, _, _, _, _, _, _, _, _, _, 8, _, _, _, 9], # 4 
    [9, 9, 9, 9, 9, _, 8, _, _, 8, 9, 8, 9, 8, _, 8, _, _, 9, 9, 8, 9, _, _, 8], # 5 
    [1, 1, 1, 1, 1, 9, 9, 9, 9, _, _, _, 9, _, _, 9, 8, _, _, _, _, 9, 9, _, 9], # 6 
    [1, 1, 9, 9, 9, 9, _, _, _, _, _, 9, _, _, _, _, _, _, 8, _, _, 8, 8, _, 9], # 7 
    [1, 1, 9, _, _, _, _, 8, 9, _, _, _, _, _, _, _, _, _, 8, _, _, 8, 9, _, 9], # 8 
    [1, 1, 9, 9, _, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, _, 1, 9, 9, 9, 9, 9, 9, 9, 9], # 9  (15, 9) vrata
    [1, 1, 9, _, _, 9, 1, 1, 1, 1, 1, 1, 9, 8, 8, _, 8, 8, 9, 1, 1, 1, 1, 1, 1], # 10
    [9, 9, _, _, 9, 9, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 6, 7, 6, 6, 6, 3], # 11
    [9, _, _, _, _, _, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 6, _, _, _, _, 3], # 12
    [9, _, 1, 1, _, _, 9, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 9, 6, _, _, _, _, 3], # 13
    [9, _, 3, 1, 1, _, 9, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 9, 6, _, _, _, _, 3], # 14 (2, 14) terminal - broj 3 u ovom redu
    [9, _, _, _, _, _, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 6, 6, 6, 6, _, 3], # 15
    [9, _, _, _, _, _, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 1, 1, 1, 6, _, 3], # 16 
    [9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 9, 1, 1, 1, 6, _, 3], # 17 
    [1, 1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 9, _, _, _, _, _, 9, 1, 1, 1, 6, _, 3], # 18 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 8, 1, 1, 1, 7, _, 3], # 19 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 1, 6, 6, 6, _, 3], # 20 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 9, 6, _, _, _, _, 3], # 21 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 9, 1, 7, 6, _, _, 3], # 22 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, _, 9, 9, 8, 1, 1, 6, _, _, 3], # 23 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 1, _, 1, 9, 9, 1, 1, 6, _, _, 3], # 24 (15, 24) vrata - za njih treba kod za ulazak koji je u terminalu
    [3, 3, 3, 3, 3, 3, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, 3], # 25 
    [3, _, _, _, 3, 3, _, 1, _, 1, 1, _, 1, _, 1, _, _, _, _, 1, 6, 1, _, _, 3], # 26 
    [3, _, _, _, 3, 3, _, 1, _, 1, 1, _, 1, _, 1, _, 1, _, _, 1, 6, 1, _, _, 3], # 27 
    [3, _, _, _, 3, 3, _, _, _, _, _, _, 1, _, _, _, 1, _, _, 1, 1, 1, _, _, 3], # 28 
    [3, _, _, _, 3, 3, _, 1, _, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 3], # 29 
    [3, _, _, _, 3, 3, _, 1, _, 6, 6, _, _, _, _, _, 1, 1, _, 1, _, _, 6, _, 3], # 30 
    [3, _, _, _, _, _, _, 1, _, 6, 6, 6, _, 6, 6, _, 1, 1, _, 1, _, _, 6, _, 3], # 31 
    [3, _, _, _, 3, 3, _, _, _, 6, 6, 6, _, 6, 7, _, _, _, _, _, 6, _, 6, _, 3], # 32
    [3, 3, 3, 3, 3, 3, _, _, _, 6, 6, 7, _, 6, 6, 6, 6, 6, _, _, 6, _, 7, _, 3], # 33
    [9, 9, 9, 9, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]  # 34
]


class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]