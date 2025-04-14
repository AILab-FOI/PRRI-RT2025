import pygame as pg
from interaction import InteractiveObject
from npc import KlonoviNPC, StakorNPC

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
            ],
            # Enemy configuration for level 1
            'enemies': {
                'count': 4,  # Number of enemies to spawn
                'types': [KlonoviNPC, StakorNPC],  # Types of enemies that can spawn
                'weights': [50, 50],  # Spawn weights for each enemy type
                'restricted_area': {(i, j) for i in range(10) for j in range(10)}  # Areas where enemies cannot spawn
            }
        }

        # Level 2 data - Odgovara mapi za level 2
        self.level_data[2] = {
            'terminals': [
                {
                    'position': (5, 5),
                    'code': '4242',
                    'unlocks_door_id': None
                },
                {
                    'position': (16, 5),
                    'code': '8888',
                    'unlocks_door_id': None
                }
            ],
            'doors': [
                {
                    'position': (11, 10),
                    'door_id': 1,
                    'requires_code': True,
                    'code': '4242'  # Koristi kod iz prvog terminala
                },
                {
                    'position': (5, 21),
                    'door_id': 2,
                    'requires_code': True,
                    'code': '8888',  # Koristi kod iz drugog terminala
                    'requires_door_id': 1  # Zahtijeva da prva vrata budu otvorena
                },
                {
                    'position': (16, 21),
                    'door_id': 3,
                    'requires_code': True,
                    'code': '4242',  # Koristi kod iz prvog terminala
                    'requires_door_id': 2  # Zahtijeva da druga vrata budu otvorena
                }
            ],
            # Enemy configuration for level 2
            'enemies': {
                'count': 6,  # More enemies in level 2
                'types': [KlonoviNPC, StakorNPC],
                'weights': [70, 30],  # More KlonoviNPC in level 2
                'restricted_area': {(i, j) for i in range(5) for j in range(5)}  # Different restricted area
            }
        }

        # Level 3 data - Only StakorNPC enemies
        self.level_data[3] = {
            'terminals': [
                {
                    'position': (5, 5),
                    'code': '9999',
                    'unlocks_door_id': None
                }
            ],
            'doors': [
                {
                    'position': (11, 10),
                    'door_id': 1,
                    'requires_code': True,
                    'code': '9999'
                }
            ],
            # Enemy configuration for level 3
            'enemies': {
                'count': 10,  # Many enemies in level 3
                'types': [StakorNPC],  # Only StakorNPC in this level
                'weights': [100],  # 100% StakorNPC
                'restricted_area': {(i, j) for i in range(3) for j in range(3)}  # Small restricted area
            }
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

    def get_enemy_config(self):
        """Get enemy configuration for the current level"""
        level_data = self.get_current_level_data()
        if level_data and 'enemies' in level_data:
            return level_data['enemies']
        # Default enemy configuration if none is specified
        return {
            'count': 4,
            'types': [KlonoviNPC, StakorNPC],
            'weights': [50, 50],
            'restricted_area': {(i, j) for i in range(10) for j in range(10)}
        }

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
        level_door_path = 'resources/sprites/static_sprites/level_door.png'

        # Use existing textures if terminal.png or door.png don't exist
        try:
            pg.image.load(terminal_path)
        except:
            terminal_path = 'resources/sprites/static_sprites/candlebra.png'

        try:
            pg.image.load(door_path)
        except:
            door_path = 'resources/sprites/static_sprites/candlebra.png'

        try:
            pg.image.load(level_door_path)
        except:
            level_door_path = door_path  # Use regular door texture if level_door.png doesn't exist

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

        # Add level exit door if this is level 1
        if self.current_level == 1:
            # Add level exit door at position (12, 34)
            level_exit = InteractiveObject(
                self.game,
                path=level_door_path,
                pos=(12, 34),
                interaction_type="level_door",
                is_level_exit=True
            )
            self.game.object_handler.add_sprite(level_exit)
            self.game.interaction.add_object(level_exit)

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

        # Scan the map for terminal (14), door (11), and level exit door objects
        terminal_positions = []
        door_positions = []
        level_exit_positions = []

        for y, row in enumerate(self.game.map.mini_map):
            for x, value in enumerate(row):
                if value == 14:  # Terminal
                    terminal_positions.append((x, y))
                elif value == 11:  # Door
                    # Check if this is the level exit door at position (12, 34)
                    if x == 12 and y == 34 and self.current_level == 1:
                        level_exit_positions.append((x, y))
                    else:
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

        # Add level exit doors
        for pos in level_exit_positions:
            level_exit = InteractiveObject(
                self.game,
                path=door_path,  # Use door texture for level exit
                pos=pos,
                interaction_type="level_door",
                is_level_exit=True
            )
            self.game.object_handler.add_sprite(level_exit)
            self.game.interaction.add_object(level_exit)

    def next_level(self):
        """Advance to the next level"""
        next_level = self.current_level + 1
        if next_level in self.level_data:
            self.current_level = next_level
            # Load the new map for this level
            self.game.map.load_level(next_level)
            # Reset the game with the new level
            self.game.new_game()
            return True
        return False
