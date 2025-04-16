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
        [9, 9, 9, 9, 9, 4, 4, 4, 4, 4, 4, 4, 16, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]  # 34 (10, 34) vrata koja se otvraju kada su svi neprijatelji porazeni na levelu)
    ],

    # Level 2 map
    
    2: [
        # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49
        [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], # 0
        [10, _, _, _, _,10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 1
        [10, _, _, _, _,10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 2
        [10, _, _, _, _,16, _, _, _, _, _, _,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], # 3
        [10,10,10,10,10,10, _, _, _, _, _, _,10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10, _, _, _, _, _, _, _,10], # 4
        [10, _, _, _, _,10, _, _, _, _, _, _,10, _,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10, _, _, _, _, _, _, _,10], # 5
        [10, _, _, _, _,10, _, _, _, _, _, _, _, _,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10, _, _, _, _, _, _, _,10], # 6
        [10,10,10,16,10,10, _, _, _, _, _, _, _, _,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10, _, _, _, _, _, _, _,10], # 7
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 8
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 9
        [10,10,10,10,10,10,10,10,10,10,10,13, _, _, _,13,10,10,10,10,10,10,13, _, _, _, _, _,13,10,10,10,10,10,13, _, _, _, _, _, _,10,10,10,10,10,10,10,10,10], # 10 Glavni Široki Hodnik 1
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 11
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 12
        [10,10,10,10,10,10,10,10,10,10,10,10, _, _, _,13,10,10,10,10,10,10,10,10,10,16,10,10,10,10,10,10,10,10,13, _, _, _, _, _, _,10,10,10,10,10,10,10,10,10], # 13 Zid s vratima za Puzzle Sobe
        [10, _, _, _, _, _, _, _, _, _, _,10, _, _, _,13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13, _, _, _, _, _, _,10, _, _, _, _, _, _, _,10], # 14 Soba 1 (Bait)
        [10, _,18,18,18,18,18,18, _, _, _,10, _, _, _,13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13, _, _, _, _, _, _,10, _,18,18,18,18,18, _,10], # 15 Promatracnice ili stakleni zidovi
        [10, _,18, _, _, _, _,18, _, _, _,10, _, _, _,13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13, _, _, _, _, _, _,10, _,18, _, _, _,16, _,10], # 16 Soba 2 (Weapon Room - Zaključana Vrata 16) - Promatracnica
        [10, _,18, _, _, _, _,16, _, _, _,16, _, _, _,16, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,16, _, _, _, _, _, _,16, _,18,18,18,18,18, _,10], # 17 Hodnik ispred soba, Vrata (16) za Weapon Room
        [10, _,18, _, _, _, _,18, _, _, _,10, _, _, _,13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13, _, _, _, _, _, _,10, _, _, _, _, _, _, _,10], # 18
        [10, _,18,18,18,18,18,18, _, _, _,10, _, _, _,13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13, _, _, _, _, _, _,10, _, _, _, _, _, _, _,10], # 19 Soba 3 (Bait)
        [10, _, _, _, _, _, _, _, _, _, _,10, _, _, _,13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13, _, _, _, _, _, _,10,10,10,10,10,10,10,10,10], # 20 Zid
        [10,10,10,10,10,10,10,10,10,10,10,10, _, _, _,13,10,10,10,10,10,10,10,10,13,16,13,10,10,10,10,10,10,10,13, _, _, _, _, _, _,10,10,10,10,10,10,10,10,10], # 21 Glavni Široki Hodnik 2 (Raskrižje u sredini)
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 22
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 23
        [10, _, _, _, _,10,10,10,10,10,10,10,10,10,10,13,13,13,13,13,13,13,13, _, _, _, _, _,13,13,13,13,13,13,13,13,13,13,13,13,10,10,10,10,10, _, _, _, _,10], # 24 Raskrižje - Centralni Hodnik
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 25
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 26
        [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10, _, _, _, _, _,13,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], # 27 Zid
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 28 Hodnik prema izlazu / mini-igri
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 29 Drugi dio zagonetke
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 30
        [10,10,10,10,10,10,10,10,10,10,10,10, _, _, _,10,10,10,10,10,10,10,10,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13, _, _, _,13,10,10,10,10], # 31 Neon Hodnik
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 32
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 33 
        [10,10,10,10,10,10,10,10,10,10,10,10, _, _, _,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10, _, _, _,13,13,13,13,13], # 34 Zid s Vratima za Izlaz (17)
        [10, _, _, _, _, _, _, _, _, _, _,10, _, _, _,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, _, _, _, _, _, _, _,13], # 35 Soba 4 (Bait) 
        [10, _, _, _, _, _, _, _, _, _, _,10, _, _, _,10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, _, _, _, _, _, _, _,13], # 36
        [10, _, _, _, _, _, _, _, _, _, _,10, _, _, _,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10, _, _, _, _, _, _, _,16], # 37 Zid Sobe 4 + Put do Izlaza X
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 38 Prazan prostor / hodnik
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 39 Treći dio zagonetke
        [10, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,10], # 40
        [13,13,13,13,13,13,13,13,13,13,13,13, _, _, _,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13, _, _, _,13,13,13,13,13], # 41
        [13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13], # 42 Velika otvorena soba / Hangar?
        [13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13], # 43 Stupovi za zaklon
        [13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13], # 44
        [13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13], # 45 Stupovi za zaklon
        [13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13], # 46 Četvrti dio zagonetke
        [13, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _,13], # 47 Neprijatelji u velikoj sobi
        [13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13], # 48 Podna rešetka s plavim svjetlom ispod?
        [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], # 49
    ],

    # Level 3 map
    3: [
        #0  1  2  3  4  5  6  7  8  9 10 11 10 13 14 15 16 17 18 19 20 21 22 23 24
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
        [7, _, _, _, _, _, _, _, _, 7, _, _, _, 7, _, _, _, _, _, _, _, _, _, _, 7], # 10
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