import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'

        # Volume settings
        self.music_volume = 0.3
        self.sfx_volume = 0.7

        # Weapon sounds
        self.pistolj = pg.mixer.Sound(self.path + 'Pistolj.wav')
        # Use the same sound for SMG for now, but play it faster
        self.smg = pg.mixer.Sound(self.path + 'Pistolj.wav')
        self.smg.set_volume(0.4 * self.sfx_volume)  # Slightly lower volume for SMG

        # NPC sounds
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_pain.set_volume(0.5 * self.sfx_volume)
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_attack = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.npc_attack.set_volume(0.5 * self.sfx_volume)

        # Štakor sounds
        self.napad_stakor = pg.mixer.Sound(self.path + 'stakor_napad.mp3')
        self.napad_stakor.set_volume(0.6 * self.sfx_volume)
        self.stakor_smrt = pg.mixer.Sound(self.path + 'stakor_smrt.mp3')

        # Weapon pickup sound
        self.weapon_pickup = pg.mixer.Sound(self.path + 'podizanje_oruzja.wav')  # Reuse pistol sound for now
        self.weapon_pickup.set_volume(0.7 * self.sfx_volume)

        # Player sounds
        self.igrac_damage = pg.mixer.Sound(self.path + 'Igrac_damage.wav')
        self.player_dash = pg.mixer.Sound(self.path + 'Dash.wav')
        self.player_dash.set_volume(0.5 * self.sfx_volume)

        # Interaction sounds
        self.terminal_beep = pg.mixer.Sound(self.path + 'terminal.wav')
        self.door_open = pg.mixer.Sound(self.path + 'vrata.wav')

        # Menu sounds - using existing sounds as placeholders
        self.menu_hover = pg.mixer.Sound(self.path + 'terminal.wav')
        self.menu_hover.set_volume(0.3 * self.sfx_volume)
        self.menu_click = pg.mixer.Sound(self.path + 'Pistolj.wav')
        self.menu_click.set_volume(0.4 * self.sfx_volume)

        # Load background music
        self.razina1 = pg.mixer.music.load(self.path + 'Pozadinska1.mp3')
        pg.mixer.music.set_volume(self.music_volume)

    def update_sfx_volume(self):
        """Update all sound effect volumes based on sfx_volume setting"""
        self.pistolj.set_volume(0.7 * self.sfx_volume)
        self.smg.set_volume(0.4 * self.sfx_volume)
        self.npc_pain.set_volume(0.5 * self.sfx_volume)
        self.npc_death.set_volume(0.7 * self.sfx_volume)
        self.npc_attack.set_volume(0.5 * self.sfx_volume)
        self.napad_stakor.set_volume(0.6 * self.sfx_volume)
        self.stakor_smrt.set_volume(0.7 * self.sfx_volume)
        self.weapon_pickup.set_volume(0.7 * self.sfx_volume)
        self.igrac_damage.set_volume(0.7 * self.sfx_volume)
        self.player_dash.set_volume(0.5 * self.sfx_volume)
        self.terminal_beep.set_volume(0.7 * self.sfx_volume)
        self.door_open.set_volume(0.7 * self.sfx_volume)
        self.menu_hover.set_volume(0.3 * self.sfx_volume)
        self.menu_click.set_volume(0.4 * self.sfx_volume)