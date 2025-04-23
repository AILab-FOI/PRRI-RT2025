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

        self.music_volume = 0.1
        self.sfx_volume = 0.7

        # Sound volume factors
        self.volume_factors = {
            # Weapon sounds
            'pistolj': 0.7,
            'smg': 0.4,
            'weapon_pickup': 0.7,

            # Player sounds
            'igrac_damage': 0.7,
            'player_dash': 0.5,

            # Generic NPC sounds
            'npc_pain': 0.5,
            'npc_death': 0.7,
            'npc_attack': 0.5,

            # Enemy-specific sounds
            'napad_stakor': 0.6,  # Stakor attack
            'stakor_smrt': 0.7,   # Stakor death
            'toster_attack': 0.5, # Toster attack
            'toster_death': 0.7,  # Toster death
            'parazit_attack': 0.6,# Parazit attack
            'parazit_death': 0.7, # Parazit death
            'jazavac_attack': 0.5,# Jazavac attack
            'jazavac_death': 0.7, # Jazavac death

            # Interaction sounds
            'terminal_beep': 0.7,
            'door_open': 0.7,

            # Powerup sounds
            'powerup_pickup': 0.7,
            'powerup_active': 0.7,
            'powerup_end': 0.6,

            # Menu sounds
            'menu_hover': 0.3,
            'menu_click': 0.4
        }

        # ===== WEAPON SOUNDS =====
        self.pistolj = self.load_sound('Pistolj.wav', self.volume_factors['pistolj'])
        self.smg = self.load_sound('Puska.wav', self.volume_factors['smg'])
        self.weapon_pickup = self.load_sound('podizanje_oruzja.wav', self.volume_factors['weapon_pickup'])

        # ===== PLAYER SOUNDS =====
        self.igrac_damage = self.load_sound('Igrac_damage.wav', self.volume_factors['igrac_damage'])
        self.player_dash = self.load_sound('Dash.wav', self.volume_factors['player_dash'])

        # ===== ENEMY SOUNDS =====
        # Generic NPC sounds
        self.npc_pain = self.load_sound('npc_pain.wav', self.volume_factors['npc_pain'])
        self.npc_death = self.load_sound('npc_death.wav', self.volume_factors['npc_death'])
        self.npc_attack = self.load_sound('npc_attack.wav', self.volume_factors['npc_attack'])

        # Stakor sounds
        self.napad_stakor = self.load_sound('stakor_napad.mp3', self.volume_factors['napad_stakor'])
        self.stakor_smrt = self.load_sound('stakor_smrt.mp3', self.volume_factors['stakor_smrt'])

        # Toster sounds (reusing existing sounds but with different volume factors)
        self.toster_attack = self.load_sound('toster_napad.wav', self.volume_factors['toster_attack'])
        self.toster_death = self.load_sound('npc_death.wav', self.volume_factors['toster_death'])

        # Parazit sounds (reusing existing sounds but with different volume factors)
        self.parazit_attack = self.load_sound('stakor_napad.mp3', self.volume_factors['parazit_attack'])
        self.parazit_death = self.load_sound('npc_death.wav', self.volume_factors['parazit_death'])

        # Jazavac sounds (reusing existing sounds but with different volume factors)
        self.jazavac_attack = self.load_sound('npc_attack.wav', self.volume_factors['jazavac_attack'])
        self.jazavac_death = self.load_sound('npc_death.wav', self.volume_factors['jazavac_death'])

        # ===== INTERACTION SOUNDS =====
        self.terminal_beep = self.load_sound('terminal.wav', self.volume_factors['terminal_beep'])
        self.door_open = self.load_sound('vrata.wav', self.volume_factors['door_open'])

        # ===== POWERUP SOUNDS =====
        self.powerup_pickup = self.load_sound('powerup_pickup.wav', self.volume_factors['powerup_pickup'])
        self.powerup_active = self.load_sound('powerup1_trajanje.wav', self.volume_factors['powerup_active'])
        self.powerup_end = self.load_sound('powerup_gasenje.wav', self.volume_factors['powerup_end'])

        # ===== MENU SOUNDS =====
        self.menu_hover = self.load_sound('menu_hover.mp3', self.volume_factors['menu_hover'])
        self.menu_click = self.load_sound('menu_klik.wav', self.volume_factors['menu_click'])

        # ===== BACKGROUND MUSIC =====
        self.razina1 = pg.mixer.music.load(self.path + 'Pozadinska1.mp3')
        pg.mixer.music.set_volume(self.music_volume)

    def update_sfx_volume(self):
        """Update all sound effect volumes based on sfx_volume setting"""
        # Use a dictionary to map sound attributes to their volume factors
        sounds = {
            # Weapon sounds
            'pistolj': self.pistolj,
            'smg': self.smg,
            'weapon_pickup': self.weapon_pickup,

            # Player sounds
            'igrac_damage': self.igrac_damage,
            'player_dash': self.player_dash,

            # Generic NPC sounds
            'npc_pain': self.npc_pain,
            'npc_death': self.npc_death,
            'npc_attack': self.npc_attack,

            # Enemy-specific sounds
            'napad_stakor': self.napad_stakor,
            'stakor_smrt': self.stakor_smrt,
            'toster_attack': self.toster_attack,
            'toster_death': self.toster_death,
            'parazit_attack': self.parazit_attack,
            'parazit_death': self.parazit_death,
            'jazavac_attack': self.jazavac_attack,
            'jazavac_death': self.jazavac_death,

            # Interaction sounds
            'terminal_beep': self.terminal_beep,
            'door_open': self.door_open,

            # Powerup sounds
            'powerup_pickup': self.powerup_pickup,
            'powerup_active': self.powerup_active,
            'powerup_end': self.powerup_end,

            # Menu sounds
            'menu_hover': self.menu_hover,
            'menu_click': self.menu_click
        }

        for sound_name, sound in sounds.items():
            sound.set_volume(self.volume_factors[sound_name] * self.sfx_volume)