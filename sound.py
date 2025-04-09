import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.pistolj = pg.mixer.Sound(self.path + 'Pistolj.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_pain.set_volume(0.4)   
        self.stakor_smrt = pg.mixer.Sound(self.path + 'stakor_smrt.mp3') 
        self.npc_shot = pg.mixer.Sound(self.path + 'stakor_napad.mp3')
        self.npc_shot.set_volume(0.7) 
        self.igrac_damage = pg.mixer.Sound(self.path + 'Igrac_damage.wav')
        self.razina1 = pg.mixer.music.load(self.path + 'Pozadinska1.mp3')
        self.player_dash = pg.mixer.Sound(self.path + 'Dash.wav')  
        self.player_dash.set_volume(0.5) 
        pg.mixer.music.set_volume(0.3)