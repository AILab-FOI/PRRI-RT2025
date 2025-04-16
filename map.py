import pygame as pg

_ = False

# Define maps for different levels
MAPS = {
    # Level 1 map
    1: [
        #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
        [9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 8, 9, 9, 9, 8, 9, 9, 9, 8, 9, 9, 9, 9, 9], # 0 ispod ovog 1. sektor
        [9, _, _, _, 9, _, _, _, _, _, _, 9, _, _, _, _, _, _, _, _, _, _, _, _, 9], # 1
        [9, _, _, _, 9, _, 9, 8, 9, 9, _, _, _, 7, _, _, _, _, 7, _, _, 7, 7, _, 8], # 2
        [9, _, _, _, _, _, 9, _, _, _, _, 7, 7, 7, 7, 7, 7, 7, _, _, _, _, 7, _, 9], # 3
        [9, _, _, _, 9, _, _, _, 8, 8, _, _, _, _, _, _, _, _, _, _, 8, _, _, _, 9], # 4
        [9, 9, 9, 9, 9, _, 8, _, _, 8, 9, 9, 8, 8, _, 7, _, _, 9, 9, 8, 9, _, _, 8], # 5
        [1, 1, 1, 1, 1, 9, 9, 8, 9, _, _, _, 7, _, _, 7, 7, _, _, _, _, 9, 9, _, 9], # 6
        [1, 1, 9, 9, 9, 9, _, _, _, _, _, 7, _, _, _, _, _, _, 9, _, _, 8, 8, _, 9], # 7
        [1, 1, 9, _, _, _, _, 8, 8, _, _, _, _, _, _, _, _, _, 9, _, _, 8, 9, _, 9], # 8
        [1, 1, 9, 9, _, 9, 9, 9, 7, 7, 7, 7, 7, 7, 7, 11, 7, 7, 8, 8, 9, 9, 8, 9, 9], # 9  (15, 9) vrata - ispod ovog 2. sektor
        [1, 1, 9, _, _, 9, 1, 1, 1, 1, 1, 1, 9, 8, 8, _, 8, 8, 9, 1, 1, 1, 1, 1, 1], # 10
        [9, 9, _, _, 9, 9, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 2, 2, 2, 2, 2, 2], # 11
        [9, _, _, _, _, _, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 2, _, _, _, _, 2], # 12
        [9, _, 7, 7, _, _, 9, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 9, 2, _, _, _, _, 2], # 13
        [9, _, 14, 7, 7, _, 9, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 9, 2, _, _, _, _, 2], # 14 (2, 14) terminal - broj 14 u ovom redu
        [9, _, _, _, _, _, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 6, 2, 2, 2, _, 2], # 15
        [9, _, _, _, _, _, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 1, 1, 1, 1, _, 8], # 16
        [9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 9, 1, 1, 1, 1, _, 8], # 17
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 9, 1, 1, 1, 1, _, 8], # 18
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 8, 1, 1, 1, 1, _, 8], # 19
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 8, 1, 1, 1, 1, _, 8], # 20
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, _, _, _, _, _, 9, 1, _, _, _, _, 8], # 21
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, _, _, _, _, _, 9, 1, 1, 1, _, _, 8], # 22
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, _, 8, 9, 8, 1, 1, 1, _, _, 8], # 23 ispod ovog 3. sektor
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7, 11, 7, 7, 7, 9, 1, 1, _, _, 8], # 24 (15, 24) vrata - za njih treba kod za ulazak koji je u terminalu
        [2, 2, 2, 2, 2, 1, _, 1, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, _, _, 8], # 25
        [2, _, _, _, 2, 1, _, 1, _, 1, 1, _, 1, _, 1, _, _, _, _, 1, 1, 1, _, _, 8], # 26
        [2, _, _, _, 2, 1, _, 1, _, 1, 1, _, 1, _, 1, _, 1, _, _, 1, 1, 1, _, _, 8], # 27
        [2, _, _, _, 2, 1, _, _, _, _, _, _, 1, _, _, _, 1, _, _, 1, 1, 1, _, _, 8], # 28
        [2, _, _, _, 2, 1, _, 1, _, _, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 8], # 29
        [2, _, _, _, 2, 1, _, 1, _, 1, 1, _, _, _, _, _, 1, 1, _, 1, _, _, 1, _, 8], # 30
        [2, _, _, _, _, _, _, 1, _, 1, 6, 1, _, 1, 1, _, 1, 1, _, 1, _, _, 1, _, 8], # 31
        [2, _, _, _, 2, 1, _, _, _, 4, 6, 4, _, 4, 1, _, _, _, _, _, 4, _, 4, _, 8], # 32
        [2, 2, 2, 2, 2, 1, _, _, _, 4, 6, 4, _, 17, 1, 1, 1, 4, _, _, 4, _, 4, _, 8], # 33
        [9, 9, 9, 9, 9, 4, 4, 4, 4, 4, 4, 4, 16, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]  # 34 (12, 34) vrata koja se otvraju kada su svi neprijatelji porazeni na levelu)
    ],

    # Level 2 map
    2: [
        #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], # 0
        [8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 8], # 1
        [8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 8], # 2
        [8, _, _, 9, 9, 9, 9, 9, _, _, _, _, _, _, 9, 9, 9, 9, 9, _, _, _, _, _, 8], # 3
        [8, _, _, 9, _, _, _, 9, _, _, _, _, _, _, 9, _, _, _, 9, _, _, _, _, _, 8], # 4
        [8, _, _, 9, _, 14, _,_, _, _, _, _, _, _, 9, _, 14, _, _, _, _, _, _, _, 8], # 5 (5, 5) i (16, 5) terminali
        [8, _, _, 9, _, _, _, 9, _, _, _, _, _, _, 9, _, _, _, 9, _, _, _, _, _, 8], # 6
        [8, _, _, 9, 9, 9, 9, 9, _, _, _, _, _, _, 9, 9, 9, 9, 9, _, _, _, _, _, 8], # 7
        [8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 8], # 8
        [8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 8], # 9
        [8, _, _, _, _, _, _, _, _, 9, 9, 11, 9, 9, _, _, _, _, _, _, _, _, _, _, 8], # 10 (11, 10) vrata
        [8, _, _, _, _, _, _, _, _, 9, _, _, _, 9, _, _, _, _, _, _, _, _, _, _, 8], # 11
        [8, _, _, _, _, _, _, _, _, 9, _, _, _, 9, _, _, _, _, _, _, _, _, _, _, 8], # 12
        [8, _, _, _, _, _, _, _, _, 9, _, _, _, 9, _, _, _, _, _, _, _, _, _, _, 8], # 13
        [8, _, _, _, _, _, _, _, _, 9, 9, 9, 9, 9, _, _, _, _, _, _, _, _, _, _, 8], # 14
        [8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 8], # 15
        [8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 8], # 16
        [8, _, _, 9, 9, 9, 9, 9, _, _, _, _, _, _, 9, 9, 9, 9, 9, _, _, _, _, _, 8], # 17
        [8, _, _, 9, _, _, _, 9, _, _, _, _, _, _, 9, _, _, _, 9, _, _, _, _, _, 8], # 18
        [8, _, _, 9, _, _, _, 9, _, _, _, _, _, _, 9, _, _, _, 9, _, _, _, _, _, 8], # 19
        [8, _, _, 9, _, _, _, 9, _, _, _, _, _, _, 9, _, _, _, 9, _, _, _, _, _, 8], # 20
        [8, _, _, 9, 9, 11, 9, 9, _, _, _, _, _, _, 9, 9, 11, 9, 9, _, _, _, _, _, 8], # 21 (5, 21) i (16, 21) vrata
        [8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 8], # 22
        [8, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 8], # 23
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]  # 24
    ],

    # Level 3 map
    3: [
        #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], # 0
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 1
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 2
        [7, _, _, 7, 7, 7, 7, 7, _, _, _, _, _, _, 7, 7, 7, 7, 7, _, _, _, _, _, 7], # 3
        [7, _, _, 7, _, _, _, 7, _, _, _, _, _, _, 7, _, _, _, 7, _, _, _, _, _, 7], # 4
        [7, _, _, 7, _, 14, _, 7, _, _, _, _, _, _, 7, _, _, _, 7, _, _, _, _, _, 7], # 5 (5, 5) terminal
        [7, _, _, 7, _, _, _, 7, _, _, _, _, _, _, 7, _, _, _, 7, _, _, _, _, _, 7], # 6
        [7, _, _, 7, 7, 7, 7, 7, _, _, _, _, _, _, 7, 7, 7, 7, 7, _, _, _, _, _, 7], # 7
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 8
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 9
        [7, _, _, _, _, _, _, _, _, 7, 7, 11, 7, 7, _, _, _, _, _, _, _, _, _, _, 7], # 10 (11, 10) vrata
        [7, _, _, _, _, _, _, _, _, 7, _, _, _, 7, _, _, _, _, _, _, _, _, _, _, 7], # 11
        [7, _, _, _, _, _, _, _, _, 7, _, _, _, 7, _, _, _, _, _, _, _, _, _, _, 7], # 12
        [7, _, _, _, _, _, _, _, _, 7, _, _, _, 7, _, _, _, _, _, _, _, _, _, _, 7], # 13
        [7, _, _, _, _, _, _, _, _, 7, 7, 7, 7, 7, _, _, _, _, _, _, _, _, _, _, 7], # 14
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 15
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 16
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 17
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 18
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 19
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 20
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 21
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 22
        [7, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 7], # 23
        [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]  # 24
    ]
}


class Map:
    def __init__(self, game):
        self.game = game
        self.level = 1
        self.load_level(self.level)

    def load_level(self, level):
        """Load a specific level map"""
        if level in MAPS:
            self.level = level
            self.mini_map = MAPS[level]
            self.world_map = {}
            self.rows = len(self.mini_map)
            self.cols = len(self.mini_map[0])
            self.get_map()
            return True
        else:
            print(f"Error: Level {level} not found")
            return False

    def get_map(self):
        """Build world_map dictionary from mini_map"""
        self.world_map = {}
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value