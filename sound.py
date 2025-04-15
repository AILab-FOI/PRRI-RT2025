import pygame as pg


class Sound:
    def load_sound(self, filename, volume_factor=1.0):
        """Helper method to load a sound and set its volume"""
        sound = pg.mixer.Sound(self.path + filename)
        sound.set_volume(volume_factor * self.sfx_volume)
        return sound

    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'

        # Volume settings
        self.music_volume = 0.3
        self.sfx_volume = 0.7

        # Sound volume factors
        self.volume_factors = {
            'pistolj': 0.7,
            'smg': 0.4,
            'npc_pain': 0.5,
            'npc_death': 0.7,
            'npc_attack': 0.5,
            'napad_stakor': 0.6,
            'stakor_smrt': 0.7,
            'weapon_pickup': 0.7,
            'igrac_damage': 0.7,
            'player_dash': 0.5,
            'terminal_beep': 0.7,
            'door_open': 0.7,
            'powerup_pickup': 0.7,
            'powerup_active': 0.4,
            'powerup_end': 0.6,
            'menu_hover': 0.3,
            'menu_click': 0.4
        }

        # Weapon sounds
        self.pistolj = self.load_sound('Pistolj.wav', self.volume_factors['pistolj'])
        self.smg = self.load_sound('Puska.wav', self.volume_factors['smg'])

        self.weapon_pickup = self.load_sound('podizanje_oruzja.wav', self.volume_factors['weapon_pickup'])

        # NPC sounds
        self.npc_pain = self.load_sound('npc_pain.wav', self.volume_factors['npc_pain'])
        self.npc_death = self.load_sound('npc_death.wav', self.volume_factors['npc_death'])
        self.npc_attack = self.load_sound('npc_attack.wav', self.volume_factors['npc_attack'])

        # Štakor sounds
        self.napad_stakor = self.load_sound('stakor_napad.mp3', self.volume_factors['napad_stakor'])
        self.stakor_smrt = self.load_sound('stakor_smrt.mp3', self.volume_factors['stakor_smrt'])

        # Player sounds
        self.igrac_damage = self.load_sound('Igrac_damage.wav', self.volume_factors['igrac_damage'])
        self.player_dash = self.load_sound('Dash.wav', self.volume_factors['player_dash'])

        # Interaction sounds
        self.terminal_beep = self.load_sound('terminal.wav', self.volume_factors['terminal_beep'])
        self.door_open = self.load_sound('vrata.wav', self.volume_factors['door_open'])

        # Powerup sounds 
        self.powerup_pickup = self.load_sound('powerup_pickup.wav', self.volume_factors['powerup_pickup'])
        self.powerup_active = self.load_sound('powerup1_trajanje.mp3', self.volume_factors['powerup_active'])
        self.powerup_end = self.load_sound('powerup_gasenje.wav', self.volume_factors['powerup_end'])

        # Menu sounds 
        self.menu_hover = self.load_sound('menu_hover.mp3', self.volume_factors['menu_hover'])
        self.menu_click = self.load_sound('menu_klik.wav', self.volume_factors['menu_click'])

        # Load background music
        self.razina1 = pg.mixer.music.load(self.path + 'Pozadinska1.mp3')
        pg.mixer.music.set_volume(self.music_volume)

    def update_sfx_volume(self):
        """Update all sound effect volumes based on sfx_volume setting"""
        # Use a dictionary to map sound attributes to their volume factors
        sounds = {
            'pistolj': self.pistolj,
            'smg': self.smg,
            'npc_pain': self.npc_pain,
            'npc_death': self.npc_death,
            'npc_attack': self.npc_attack,
            'napad_stakor': self.napad_stakor,
            'stakor_smrt': self.stakor_smrt,
            'weapon_pickup': self.weapon_pickup,
            'igrac_damage': self.igrac_damage,
            'player_dash': self.player_dash,
            'terminal_beep': self.terminal_beep,
            'door_open': self.door_open,
            'menu_hover': self.menu_hover,
            'menu_click': self.menu_click,
            'powerup_pickup': self.powerup_pickup,
            'powerup_active': self.powerup_active,
            'powerup_end': self.powerup_end
        }

        # Update volume for each sound
        for sound_name, sound in sounds.items():
            sound.set_volume(self.volume_factors[sound_name] * self.sfx_volume)