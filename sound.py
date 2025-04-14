import pygame as pg
import os


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.sounds = {}  # Dictionary to store loaded sounds

        # Define sound configurations
        sound_configs = {
            'pistolj': {'file': 'Pistolj.wav', 'volume': 1.0},
            'npc_pain': {'file': 'npc_pain.wav', 'volume': 0.5},
            'npc_death': {'file': 'npc_death.wav', 'volume': 1.0},
            'npc_attack': {'file': 'npc_attack.wav', 'volume': 0.5},
            'napad_stakor': {'file': 'stakor_napad.mp3', 'volume': 0.6},
            'stakor_smrt': {'file': 'stakor_smrt.mp3', 'volume': 1.0},
            'igrac_damage': {'file': 'Igrac_damage.wav', 'volume': 1.0},
            'player_dash': {'file': 'Dash.wav', 'volume': 0.5},
            'terminal_beep': {'file': 'terminal_beep.wav', 'volume': 1.0, 'fallback': 'pistolj'},
            'door_open': {'file': 'door_open.wav', 'volume': 1.0, 'fallback': 'player_dash'}
        }

        # Load all sounds
        self.load_sounds(sound_configs)

        # Load background music
        try:
            pg.mixer.music.load(self.path + 'Pozadinska1.mp3')
            pg.mixer.music.set_volume(0.3)
        except Exception as e:
            print(f"Error loading background music: {e}")

    def load_sounds(self, sound_configs):
        """Load all sounds based on configuration"""
        for sound_name, config in sound_configs.items():
            file_path = self.path + config['file']

            try:
                if os.path.exists(file_path):
                    sound = pg.mixer.Sound(file_path)
                    sound.set_volume(config['volume'])
                    self.sounds[sound_name] = sound
                else:
                    # If file doesn't exist, use fallback if specified
                    if 'fallback' in config and config['fallback'] in self.sounds:
                        print(f"Warning: Sound file {file_path} not found, using fallback")
                        self.sounds[sound_name] = self.sounds[config['fallback']]
                    else:
                        print(f"Warning: Sound file {file_path} not found")
            except Exception as e:
                print(f"Error loading sound {file_path}: {e}")
                # If loading fails, use fallback if specified
                if 'fallback' in config and config['fallback'] in self.sounds:
                    self.sounds[sound_name] = self.sounds[config['fallback']]

        # Create properties for backward compatibility
        for sound_name in sound_configs.keys():
            if sound_name in self.sounds:
                setattr(self, sound_name, self.sounds[sound_name])
            else:
                # Create a dummy sound object if loading failed
                setattr(self, sound_name, DummySound())


class DummySound:
    """A dummy sound class that does nothing when played"""
    def play(self):
        pass

    def set_volume(self, _):
        pass