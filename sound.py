import pygame as pg
import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Sound:
    def load_sound(self, filename, volume_factor=1.0):
        """Helper method to load a sound and set its volume"""
        try:
            sound_path = resource_path(os.path.join(self.path, filename))
            sound = pg.mixer.Sound(sound_path)
            sound.set_volume(volume_factor * self.sfx_volume)
            return sound
        except Exception:
            # Za sve greške, koristi placeholder
            try:
                sound_path = resource_path(os.path.join(self.path, 'crash.wav'))
                sound = pg.mixer.Sound(sound_path)
                sound.set_volume(volume_factor * self.sfx_volume)
                return sound
            except Exception:
                # Ako ni placeholder ne radi, vrati None
                return None

    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound'

        self.music_volume = 0.1
        self.sfx_volume = 0.7

        # Sound volume factors
        self.volume_factors = {
            # Weapon sounds
            'pistolj': 0.7,
            'smg': 0.4,
            'plasmagun': 0.6,
            'weapon_pickup': 0.7,

            # Player sounds
            'igrac_damage': 0.7,
            'player_dash': 0.5,

            # Generic NPC sounds
            'npc_pain': 0.5,
            'npc_death': 0.9,
            'npc_attack': 0.5,

            # Enemy-specific sounds
            'napad_stakor': 0.6,  # Stakor attack
            'stakor_smrt': 0.9,   # Stakor death

            'toster_attack': 0.5, # Toster attack
            'toster_death': 0.9,  # Toster death
            'toster_damage': 0.5,  # Toster damage

            'parazit_attack': 0.6,# Parazit attack
            'parazit_death': 0.9, # Parazit death
            'parazit_damage': 0.5, # Parazit damage

            'jazavac_attack': 0.5,# Jazavac attack
            'jazavac_death': 0.9, # Jazavac death
            'jazavac_damage': 0.5, # Jazavac damage

            'madrac_attack': 0.6,# Madrac attack
            'madrac_death': 0.9, # Madrac death
            'madrac_damage': 0.5, # Madrac damage

            'boss_attack': 0.7,# Boss attack
            'boss_death': 1.0, # Boss death
            'boss_damage': 0.6, # Boss damage

            # Interaction sounds
            'terminal_beep': 0.7,
            'door_open': 0.7,

            # Powerup sounds
            'powerup_pickup': 0.7,
            'powerup_active': 0.7,
            'powerup_end': 0.6,

            # Menu sounds
            'menu_hover': 0.3,
            'menu_click': 0.4,

            # Dialogue sounds
            'dialogue_line': 0.7
        }

        # ===== WEAPON SOUNDS =====
        self.pistolj = self.load_sound('Pistolj.wav', self.volume_factors['pistolj'])
        self.smg = self.load_sound('Puska.wav', self.volume_factors['smg'])
        self.plasmagun = self.load_sound('Puska.wav', self.volume_factors['plasmagun'])
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

        # Toster sounds
        self.toster_attack = self.load_sound('toster_napad.wav', self.volume_factors['toster_attack'])
        self.toster_death = self.load_sound('toster_smrt.mp3', self.volume_factors['toster_death'])
        self.toster_damage = self.load_sound('toster_damage.wav', self.volume_factors['toster_damage'])

        # Parazit sounds
        self.parazit_attack = self.load_sound('parazit_napad.mp3', self.volume_factors['parazit_attack'])
        self.parazit_death = self.load_sound('parazit_smrt.wav', self.volume_factors['parazit_death'])
        self.parazit_damage = self.load_sound('parazit_damage.mp3', self.volume_factors['parazit_damage'])

        # Jazavac sounds (reusing existing sounds but with different volume factors)
        self.jazavac_attack = self.load_sound('jazavac_napad.wav', self.volume_factors['jazavac_attack'])
        self.jazavac_death = self.load_sound('jazavac_smrt.wav', self.volume_factors['jazavac_death'])
        self.jazavac_damage = self.load_sound('jazavac_damage.wav', self.volume_factors['jazavac_damage'])

        # Madrac sounds
        self.madrac_attack = self.load_sound('madrac_napad.wav', self.volume_factors['madrac_attack'])
        self.madrac_death = self.load_sound('madrac_smrt.wav', self.volume_factors['madrac_death'])
        self.madrac_damage = self.load_sound('madrac_damage.wav', self.volume_factors['madrac_damage'])

        # Boss sounds
        self.boss_attack = self.load_sound('boss_napad.wav', self.volume_factors['boss_attack'])
        self.boss_death = self.load_sound('boss_smrt.wav', self.volume_factors['boss_death'])
        self.boss_damage = self.load_sound('boss_damage.wav', self.volume_factors['boss_damage'])

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

        # ===== DIALOGUE SOUNDS =====
        # Placeholder zvuk za dijalog - koristimo crash.wav za sve linije
        self.dialogue_line = self.load_sound('crash.wav', self.volume_factors['dialogue_line'])

        # Rječnik za pohranu zvukova dijaloga
        # Ključevi će biti u formatu 'dialogue_id_line_index' (npr. 'marvin_intro_0')
        self.dialogue_sounds = {}

        # Inicijaliziraj direktorij za zvučne datoteke dijaloga
        self.init_dialogue_directories()

        # ===== BACKGROUND MUSIC =====
        # Putanje do pozadinskih glazbi za svaku razinu
        self.background_music = {
            1: 'Pozadinska1.mp3',
            2: 'Pozadinska2.wav',
            3: 'Pozadinska3.mp3',
            4: 'Pozadinska4.wav',
            5: 'Pozadinska5.wav'
        }

        # Učitaj glazbu za prvu razinu kao početnu
        self.current_music_level = 1
        music_path = resource_path(os.path.join(self.path, self.background_music[1]))
        pg.mixer.music.load(music_path)
        pg.mixer.music.set_volume(self.music_volume)

    def init_dialogue_directories(self):
        """Initialize directories for dialogue sounds"""
        # When running as executable, we don't need to create directories
        # as all resources are already packaged
        if getattr(sys, 'frozen', False):
            return

        # Only create directories when running in development mode
        # Glavni direktorij za zvukove dijaloga
        dialogue_dir = os.path.join(self.path, "dialogues")
        if not os.path.exists(dialogue_dir):
            os.makedirs(dialogue_dir, exist_ok=True)

        # Direktoriji za svaki dijalog
        for dialogue_id in ["marvin_intro", "level2_puzzle", "marvin_ending"]:
            dialogue_subdir = os.path.join(dialogue_dir, dialogue_id)
            if not os.path.exists(dialogue_subdir):
                os.makedirs(dialogue_subdir, exist_ok=True)

        # Kopiraj crash.wav kao placeholder za svaku liniju dijaloga
        self.create_placeholder_dialogue_sounds()

    def create_placeholder_dialogue_sounds(self):
        """Create placeholder sound files for each dialogue line"""
        import os
        import shutil

        # Putanja do placeholder zvuka
        placeholder_path = os.path.join(self.path, "crash.wav")

        # Provjeri postoji li placeholder zvuk
        if not os.path.exists(placeholder_path):
            return

        # Dijalozi i broj linija
        dialogues = {
            "marvin_intro": 9,
            "level2_puzzle": 11,
            "marvin_ending": 11
        }

        # Kopiraj placeholder zvuk za svaku liniju dijaloga
        for dialogue_id, num_lines in dialogues.items():
            dialogue_dir = os.path.join(self.path, "dialogues", dialogue_id)
            for i in range(num_lines):
                target_path = os.path.join(dialogue_dir, f"{i}.wav")
                # Kopiraj samo ako datoteka ne postoji
                if not os.path.exists(target_path):
                    try:
                        shutil.copy(placeholder_path, target_path)
                    except Exception:
                        pass

    def get_dialogue_sound(self, dialogue_id, line_index, speaker=None):
        """Get sound for a specific dialogue line, loading it if necessary"""
        sound_key = f"{dialogue_id}_{line_index}"

        # Ako zvuk već postoji u rječniku, vrati ga
        if sound_key in self.dialogue_sounds:
            return self.dialogue_sounds[sound_key]

        # Posebna obrada za marvin_intro, level2_puzzle i marvin_ending dijaloge
        if (dialogue_id == "marvin_intro" or dialogue_id == "level2_puzzle" or dialogue_id == "marvin_ending") and speaker:
            try:
                # Brojimo koliko puta se svaki govornik pojavio do trenutne linije
                speaker_count = 0

                # Učitaj dijalog iz JSON datoteke
                import json
                import os
                dialogue_path = resource_path(os.path.join('resources', 'dialogues', f"{dialogue_id}.json"))
                with open(dialogue_path, 'r') as f:
                    dialogue_data = json.load(f)

                # Broji koliko puta se govornik pojavio do trenutne linije
                for i in range(line_index + 1):
                    if i < len(dialogue_data["speakers"]) and dialogue_data["speakers"][i] == speaker:
                        speaker_count += 1

                # Odredi putanju do zvučne datoteke ovisno o dijalogu
                prefix = ""
                if dialogue_id == "marvin_intro":
                    prefix = "Intro_"
                elif dialogue_id == "level2_puzzle":
                    prefix = "Puzzle_"
                elif dialogue_id == "marvin_ending":
                    prefix = "Ending_"
                else:
                    # Ako dijalog nije podržan, koristi placeholder
                    return self.dialogue_line

                if speaker == "Arthur":
                    sound_path = f"{prefix}Arthur{speaker_count}.mp3"
                elif speaker == "Marvin":
                    sound_path = f"{prefix}Marvin{speaker_count}.mp3"
                else:
                    # Ako govornik nije Arthur ili Marvin, koristi placeholder
                    return self.dialogue_line

                # Učitaj zvuk
                sound = self.load_sound(sound_path, self.volume_factors['dialogue_line'])
                self.dialogue_sounds[sound_key] = sound
                return sound
            except Exception:
                return self.dialogue_line

        # Za ostale dijaloge, pokušaj učitati zvuk iz direktorija dialogues
        try:
            # Putanja do zvučne datoteke: resources/sound/dialogues/dialogue_id/line_index.wav
            # Npr. resources/sound/dialogues/marvin_intro/0.wav
            sound_path = f"dialogues/{dialogue_id}/{line_index}.wav"

            # Pokušaj učitati zvuk
            sound = self.load_sound(sound_path, self.volume_factors['dialogue_line'])
            self.dialogue_sounds[sound_key] = sound
            return sound
        except Exception:
            # Ako zvuk ne postoji, koristi placeholder
            return self.dialogue_line

    def update_sfx_volume(self):
        """Update all sound effect volumes based on sfx_volume setting"""
        # Use a dictionary to map sound attributes to their volume factors
        sounds = {
            # Weapon sounds
            'pistolj': self.pistolj,
            'smg': self.smg,
            'plasmagun': self.plasmagun,
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
            'toster_damage': self.toster_damage,

            'parazit_attack': self.parazit_attack,
            'parazit_death': self.parazit_death,
            'parazit_damage': self.parazit_damage,

            'jazavac_attack': self.jazavac_attack,
            'jazavac_death': self.jazavac_death,
            'jazavac_damage': self.jazavac_damage,

            'madrac_attack': self.madrac_attack,
            'madrac_death': self.madrac_death,
            'madrac_damage': self.madrac_damage,

            'boss_attack': self.boss_attack,
            'boss_death': self.boss_death,
            'boss_damage': self.boss_damage,

            # Interaction sounds
            'terminal_beep': self.terminal_beep,
            'door_open': self.door_open,

            # Powerup sounds
            'powerup_pickup': self.powerup_pickup,
            'powerup_active': self.powerup_active,
            'powerup_end': self.powerup_end,

            # Menu sounds
            'menu_hover': self.menu_hover,
            'menu_click': self.menu_click,

            # Dialogue sounds
            'dialogue_line': self.dialogue_line
        }

        # Ažuriraj volumen za sve zvukove u rječniku
        for sound_name, sound in sounds.items():
            sound.set_volume(self.volume_factors[sound_name] * self.sfx_volume)

        # Ažuriraj volumen za sve zvukove dijaloga
        for sound_key, sound in self.dialogue_sounds.items():
            sound.set_volume(self.volume_factors['dialogue_line'] * self.sfx_volume)

    def update_music_volume(self):
        """Update background music volume based on music_volume setting"""
        pg.mixer.music.set_volume(self.music_volume)

    def change_music_for_level(self, level):
        """Change background music based on the current level"""
        if level in self.background_music and level != self.current_music_level:
            # Zaustavi trenutnu glazbu
            pg.mixer.music.stop()
            # Učitaj novu glazbu
            music_path = resource_path(os.path.join(self.path, self.background_music[level]))
            pg.mixer.music.load(music_path)
            # Postavi volumen
            pg.mixer.music.set_volume(self.music_volume)
            # Pokreni glazbu
            pg.mixer.music.play(-1)  # -1 znači beskonačno ponavljanje
            # Ažuriraj trenutnu razinu glazbe
            self.current_music_level = level