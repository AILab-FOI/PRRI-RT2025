import pygame as pg
from interaction import InteractiveObject

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.current_level = 1
        self.level_data = {}
        self.initialize_levels()

    def initialize_levels(self):
        """Initialize data for all game levels"""
        # Level 1 data
        self.level_data[1] = {
            'terminals': [
                {
                    'position': (2, 14),
                    'code': '1337',
                    'unlocks_door_id': None  # Terminal doesn't automatically unlock any doors
                }
            ],
            'doors': [
                {
                    'position': (15, 9),
                    'door_id': 1,
                    'requires_code': True,
                    'code': '1337'  # First door uses code 1337
                },
                {
                    'position': (15, 24),
                    'door_id': 2,
                    'requires_code': True,
                    'code': '1337',  # Second door also uses code 1337
                    'requires_door_id': 1  # This door requires door 1 to be opened first
                }
            ]
        }

        # Level 2 data (example for future use)
        self.level_data[2] = {
            'terminals': [
                {
                    'position': (5, 10),
                    'code': '4242',
                    'unlocks_door_id': 3
                },
                {
                    'position': (12, 18),
                    'code': '8888',
                    'unlocks_door_id': 4
                }
            ],
            'doors': [
                {
                    'position': (8, 15),
                    'door_id': 3,
                    'requires_code': True
                },
                {
                    'position': (20, 12),
                    'door_id': 4,
                    'requires_code': True
                }
            ]
        }

    def load_level(self, level_number):
        """Load a specific level"""
        if level_number in self.level_data:
            self.current_level = level_number
            return self.level_data[level_number]
        else:
            print(f"Error: Level {level_number} not found")
            return None

    def get_current_level_data(self):
        """Get data for the current level"""
        return self.level_data.get(self.current_level, None)

    def setup_interactive_objects(self):
        """Set up all interactive objects for the current level"""
        level_data = self.get_current_level_data()
        if not level_data:
            # If no level data, try to auto-detect interactive objects from the map
            self.auto_detect_interactive_objects()
            return

        # Clear existing interactive objects
        self.game.interaction.interaction_objects.clear()

        # Load terminal and door textures
        terminal_path = 'resources/sprites/static_sprites/terminal.png'
        door_path = 'resources/sprites/static_sprites/door.png'

        # Use existing textures if terminal.png or door.png don't exist
        try:
            pg.image.load(terminal_path)
        except:
            terminal_path = 'resources/sprites/static_sprites/candlebra.png'

        try:
            pg.image.load(door_path)
        except:
            door_path = 'resources/sprites/static_sprites/candlebra.png'

        # Add terminals
        for terminal_data in level_data['terminals']:
            terminal = InteractiveObject(
                self.game,
                path=terminal_path,
                pos=terminal_data['position'],
                interaction_type="terminal",
                code=terminal_data['code'],
                unlocks_door_id=terminal_data.get('unlocks_door_id')
            )
            self.game.object_handler.add_sprite(terminal)
            self.game.interaction.add_object(terminal)

        # Add doors
        for door_data in level_data['doors']:
            door = InteractiveObject(
                self.game,
                path=door_path,
                pos=door_data['position'],
                interaction_type="door",
                door_id=door_data['door_id'],
                requires_code=door_data.get('requires_code', False),
                requires_door_id=door_data.get('requires_door_id'),
                code=door_data.get('code')  # Add code for the door
            )
            self.game.object_handler.add_sprite(door)
            self.game.interaction.add_object(door)

    def auto_detect_interactive_objects(self):
        """Automatically detect interactive objects from the map"""
        # Clear existing interactive objects
        self.game.interaction.interaction_objects.clear()

        # Load terminal and door textures
        terminal_path = 'resources/sprites/static_sprites/terminal.png'
        door_path = 'resources/sprites/static_sprites/door.png'

        # Use existing textures if terminal.png or door.png don't exist
        try:
            pg.image.load(terminal_path)
        except:
            terminal_path = 'resources/sprites/static_sprites/candlebra.png'

        try:
            pg.image.load(door_path)
        except:
            door_path = 'resources/sprites/static_sprites/candlebra.png'

        # Scan the map for terminal (14) and door (11) objects
        terminal_positions = []
        door_positions = []

        for y, row in enumerate(self.game.map.mini_map):
            for x, value in enumerate(row):
                if value == 14:  # Terminal
                    terminal_positions.append((x, y))
                elif value == 11:  # Door
                    door_positions.append((x, y))

        # Create a default code
        default_code = "1337"

        # Add terminals
        for i, pos in enumerate(terminal_positions):
            terminal = InteractiveObject(
                self.game,
                path=terminal_path,
                pos=pos,
                interaction_type="terminal",
                code=default_code,
                unlocks_door_id=i+1  # Each terminal unlocks a door with ID i+1
            )
            self.game.object_handler.add_sprite(terminal)
            self.game.interaction.add_object(terminal)

        # Add doors
        for i, pos in enumerate(door_positions):
            door = InteractiveObject(
                self.game,
                path=door_path,
                pos=pos,
                interaction_type="door",
                door_id=i+1,  # Door ID i+1
                requires_code=True,
                code=default_code,  # Use the same code for all doors
                requires_door_id=i if i > 0 else None  # Each door (except first) requires previous door
            )
            self.game.object_handler.add_sprite(door)
            self.game.interaction.add_object(door)

    def next_level(self):
        """Advance to the next level"""
        next_level = self.current_level + 1
        if next_level in self.level_data:
            self.current_level = next_level
            self.game.new_game()  # Reset the game with the new level
            return True
        return False
