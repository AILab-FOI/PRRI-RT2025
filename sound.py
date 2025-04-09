import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'

        # Volume settings
        self.music_volume = 0.3
        self.sfx_volume = 0.5

        # Sound effects
        self.pistolj = pg.mixer.Sound(self.path + 'Pistolj.wav')
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_attack = pg.mixer.Sound(self.path + 'npc_attack.wav')

        # Štakor sounds
        self.napad_stakor = pg.mixer.Sound(self.path + 'stakor_napad.mp3')
        self.stakor_smrt = pg.mixer.Sound(self.path + 'stakor_smrt.mp3')

        # Player sounds
        self.igrac_damage = pg.mixer.Sound(self.path + 'Igrac_damage.wav')
        self.player_dash = pg.mixer.Sound(self.path + 'Dash.wav')

        # Menu sounds - using existing sounds as placeholders
        # In a real game, you'd use dedicated UI sound effects
        self.menu_click = self.player_dash  # Button click sound
        self.menu_hover = self.pistolj      # Button hover sound
        self.menu_hover.set_volume(0.1)     # Lower volume for hover sound

        # Load background music
        self.razina1 = pg.mixer.music.load(self.path + 'Pozadinska1.mp3')

        # Set initial volumes
        self.update_sfx_volume()
        pg.mixer.music.set_volume(self.music_volume)

    def update_sfx_volume(self):
        """Update all sound effect volumes based on sfx_volume setting"""
        self.pistolj.set_volume(self.sfx_volume)
        self.npc_pain.set_volume(self.sfx_volume * 0.5)
        self.npc_death.set_volume(self.sfx_volume)
        self.npc_attack.set_volume(self.sfx_volume * 0.5)
        self.napad_stakor.set_volume(self.sfx_volume * 0.6)
        self.stakor_smrt.set_volume(self.sfx_volume)
        self.igrac_damage.set_volume(self.sfx_volume)
        self.player_dash.set_volume(self.sfx_volume * 0.5)