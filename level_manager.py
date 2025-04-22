import os
from interaction import InteractiveObject
from npc import KlonoviNPC, StakorNPC, TosterNPC, ParazitNPC, JazavacNPC
from dialogue import create_dialogue_npcs

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.current_level = 1
        self.level_data = {}
        self.max_level = 5  # Total number of levels
        self.current_weapon_type = 'pistol'  # Default weapon type
        self.initialize_levels()

    def initialize_levels(self):
        """Initialize data for all game levels by loading from level files"""
        try:
            # Import level modules dynamically
            import importlib

            # Load each level's data
            for level_num in range(1, self.max_level + 1):
                try:
                    # Import the level module
                    level_module = importlib.import_module(f'levels.level{level_num}')

                    # Get the level data from the module
                    self.level_data[level_num] = level_module.get_level_data()
                    print(f"Loaded level {level_num} data successfully")
                except ImportError as e:
                    print(f"Error loading level {level_num}: {e}")
                    # Create an empty level structure as fallback
                    from levels.base_level import create_base_level_structure
                    self.level_data[level_num] = create_base_level_structure()
        except Exception as e:
            print(f"Error initializing levels: {e}")
            # Fallback to empty level data
            self.level_data = {i: {} for i in range(1, self.max_level + 1)}

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
            'count': 5,
            'types': [KlonoviNPC, StakorNPC, TosterNPC, ParazitNPC, JazavacNPC],
            'weights': [20, 20, 20, 20, 20],
            'restricted_area': {(i, j) for i in range(10) for j in range(10)},
            'fixed_positions': []
        }

    def get_sprite_data(self):
        """Get decorative sprite data for the current level"""
        level_data = self.get_current_level_data()
        if level_data and 'sprites' in level_data:
            return level_data['sprites']
        # Return empty list if no sprites are defined for this level
        return []

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

        # Make sure the files exist before trying to load them
        if not os.path.isfile(terminal_path):
            print(f"Warning: Terminal texture not found at {terminal_path}")

        if not os.path.isfile(door_path):
            print(f"Warning: Door texture not found at {door_path}")
            # Don't set a fallback

        if not os.path.isfile(level_door_path):
            print(f"Warning: Level door texture not found at {level_door_path}")
            level_door_path = door_path

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
                code=door_data.get('code')
            )
            self.game.object_handler.add_sprite(door)
            self.game.interaction.add_object(door)

        # Add weapon pickups if they exist in the level data
        if 'weapons' in level_data:
            for weapon_data in level_data['weapons']:
                weapon_pickup = InteractiveObject(
                    self.game,
                    path=weapon_data['path'],
                    pos=weapon_data['position'],
                    interaction_type="weapon",
                    weapon_type=weapon_data['weapon_type']
                )
                self.game.object_handler.add_sprite(weapon_pickup)
                self.game.interaction.add_object(weapon_pickup)

        # Add powerups if they exist in the level data
        if 'powerups' in level_data:
            for powerup_data in level_data['powerups']:
                self.game.object_handler.add_powerup(
                    pos=powerup_data['position'],
                    powerup_type=powerup_data['powerup_type']
                )

        # Define exit door positions for each level
        exit_positions = {
            1: (12, 34),  # Level 1 exit at position (12, 34)
            2: (31, 33),  # Level 2 exit at position (12, 20)
            3: (14, 34)   # Level 3 exit at position (12, 20)
        }

        # Add the exit door if we have a position defined for this level
        if self.current_level in exit_positions:
            exit_pos = exit_positions[self.current_level]
            level_exit = InteractiveObject(
                self.game,
                path=level_door_path,
                pos=exit_pos,
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


        # Make sure the files exist before trying to load them
        if not os.path.isfile(terminal_path):
            print(f"Warning: Terminal texture not found at {terminal_path}")
            # Don't set a fallback - better to have no sprite than wrong sprite

        if not os.path.isfile(door_path):
            print(f"Warning: Door texture not found at {door_path}")
            # Don't set a fallback

        # Scan the map for terminal (14), door (11), and level exit door objects
        terminal_positions = []
        door_positions = []
        level_exit_positions = []

        for y, row in enumerate(self.game.map.mini_map):
            for x, value in enumerate(row):
                if value == 14:  # Terminal
                    terminal_positions.append((x, y))
                elif value == 11:  # Door
                    # Define exit door positions for each level
                    exit_positions = {
                        1: (12, 34),  # Level 1 exit at position (12, 34)
                        2: (12, 20),  # Level 2 exit at position (12, 20)
                        3: (12, 20)   # Level 3 exit at position (12, 20)
                    }

                    # Check if this is a level exit door
                    current_pos = (x, y)
                    if self.current_level in exit_positions and current_pos == exit_positions[self.current_level]:
                        level_exit_positions.append(current_pos)
                    else:
                        door_positions.append(current_pos)

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
                unlocks_door_id=i+1
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
                door_id=i+1,
                requires_code=True,
                code=default_code,
                requires_door_id=i if i > 0 else None
            )
            self.game.object_handler.add_sprite(door)
            self.game.interaction.add_object(door)

        # Add level exit doors
        for pos in level_exit_positions:
            level_exit = InteractiveObject(
                self.game,
                path=door_path,
                pos=pos,
                interaction_type="level_door",
                is_level_exit=True
            )
            self.game.object_handler.add_sprite(level_exit)
            self.game.interaction.add_object(level_exit)

    def setup_dialogue_npcs(self):
        """Set up dialogue NPCs for the current level"""
        level_data = self.get_current_level_data()
        if level_data and 'dialogue_npcs' in level_data:
            # Create dialogue NPCs for the current level
            create_dialogue_npcs(self.game, level_data['dialogue_npcs'])

    def prepare_next_level(self):
        """Prepare the next level for loading but don't activate it yet"""
        next_level = self.current_level + 1
        if next_level <= self.max_level and next_level in self.level_data:
            # Store the next level number but don't change current_level yet
            self._next_level = next_level
            return True
        elif next_level > self.max_level:
            print("Congratulations! You have completed all levels!")
            return False
        return False

    def activate_next_level(self):
        """Activate the previously prepared next level"""
        if hasattr(self, '_next_level'):
            self.current_level = self._next_level
            self.game.map.load_level(self.current_level)
            return True
        return False

    def next_level(self):
        """Legacy method for backward compatibility"""
        next_level = self.current_level + 1
        if next_level <= self.max_level and next_level in self.level_data:
            self.current_level = next_level
            self.game.map.load_level(next_level)
            self.game.new_game()
            return True
        elif next_level > self.max_level:
            print("Congratulations! You have completed all levels!")
            return False
        return False
