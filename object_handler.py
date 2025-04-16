from sprite_object import *
from npc import *
from powerup import PowerUp
from random import choices


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        self.npc_positions = {}
        self.win_message_shown = False

        self.spawn_npc()

        # Load decorative sprites for the current level
        self.load_decorative_sprites()

    def spawn_npc(self):
        """Load enemy configuration and spawn NPCs based on the current level"""
        # Clear existing NPCs
        self.npc_list = []
        self.npc_positions = {}
        self.win_message_shown = False

        # Get enemy configuration from level manager
        enemy_config = self.game.level_manager.get_enemy_config()
        self.enemies = enemy_config['count']
        self.npc_types = enemy_config['types']
        self.weights = enemy_config['weights']
        self.restricted_area = enemy_config['restricted_area']
        fixed_positions = enemy_config.get('fixed_positions', [])

        # First spawn enemies at fixed positions
        for pos in fixed_positions:
            if len(self.npc_list) >= self.enemies:
                break  # Don't spawn more than the configured count

            x, y = pos
            # Skip if position is in a wall or restricted area
            if (pos in self.game.map.world_map) or (pos in self.restricted_area):
                continue

            # Choose enemy type based on weights
            npc_type = choices(self.npc_types, self.weights)[0]
            self.add_npc(npc_type(self.game, pos=(x + 0.5, y + 0.5)))

        # Then spawn remaining enemies at random positions
        remaining = self.enemies - len(self.npc_list)
        if remaining > 0:
            self._spawn_random_enemies(remaining)

    def check_win(self):
        # Get only hostile NPCs (exclude friendly NPCs like dialogue NPCs)
        hostile_npcs = [npc for npc in self.npc_list if npc.alive and not hasattr(npc, 'is_friendly')]

        # Check if all hostile enemies are defeated
        self.all_enemies_defeated = len(hostile_npcs) == 0

        # If all enemies are defeated, show a message and enable the level exit door
        if self.all_enemies_defeated and not self.win_message_shown:
            self.win_message_shown = True
            # Count only hostile enemies for the message
            hostile_count = sum(1 for npc in self.npc_list if not hasattr(npc, 'is_friendly'))
            self.game.object_renderer.show_message(f"All {hostile_count} enemies defeated! Find the exit door.")
            # Enable the level exit door
            self.enable_level_exit()

    def update(self):
        # Update NPC positions, excluding friendly NPCs for win condition checking
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}

        # Update all sprites and NPCs
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

        # Check win condition
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def enable_level_exit(self):
        """Enable the level exit door after all enemies are defeated"""
        # Find the level exit door if it exists
        for obj in self.game.interaction.interaction_objects:
            if hasattr(obj, 'is_level_exit') and obj.is_level_exit:
                obj.is_enabled = True
                # Show a message that the exit is now open
                self.game.object_renderer.show_message("The exit door is now open!")

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def add_powerup(self, pos, powerup_type='invulnerability'):
        """Add a powerup at the specified position"""
        powerup = PowerUp(self.game, pos=pos, powerup_type=powerup_type)
        self.add_sprite(powerup)
        return powerup

    def load_decorative_sprites(self):
        """Load decorative sprites for the current level"""
        # Get sprite data from level manager
        sprite_data = self.game.level_manager.get_sprite_data()

        # Add all sprites using a loop
        for sprite_info, pos in sprite_data:
            # Check if sprite_info is a tuple (folder, sprite_type) or just a string (sprite_type)
            if isinstance(sprite_info, tuple) and len(sprite_info) == 2:
                folder, sprite_type = sprite_info
                # Use the specified folder
                if folder == 'static':
                    sprite_path = self.static_sprite_path + sprite_type + '.png'
                elif folder == 'level1':
                    sprite_path = 'resources/teksture/level1/' + sprite_type + '.png'
                elif folder == 'level2':
                    sprite_path = 'resources/teksture/level2/' + sprite_type + '.png'
                elif folder == 'level3':
                    sprite_path = 'resources/teksture/level3/' + sprite_type + '.png'
                elif folder == 'level4':
                    sprite_path = 'resources/teksture/level4/' + sprite_type + '.png'
                elif folder == 'teksture':
                    sprite_path = 'resources/teksture/' + sprite_type + '.png'
                else:
                    # Default to static sprites if folder is unknown
                    sprite_path = self.static_sprite_path + sprite_type + '.png'
            else:
                # Backward compatibility: if sprite_info is just a string, use the static sprites folder
                sprite_type = sprite_info
                sprite_path = self.static_sprite_path + sprite_type + '.png'

            self.add_sprite(SpriteObject(self.game, path=sprite_path, pos=pos))

    def _spawn_random_enemies(self, count):
        """Helper method to spawn a given number of enemies at random positions"""
        # Create a list of valid spawn positions
        valid_positions = []
        for y in range(self.game.map.rows):
            for x in range(self.game.map.cols):
                pos = (x, y)
                if (pos not in self.game.map.world_map) and (pos not in self.restricted_area):
                    valid_positions.append(pos)

        # Shuffle the valid positions to randomize spawning
        from random import shuffle
        shuffle(valid_positions)

        # Spawn enemies at valid positions
        spawned = 0
        for pos in valid_positions:
            if spawned >= count:
                break

            x, y = pos
            # Choose enemy type based on weights
            npc_type = choices(self.npc_types, self.weights)[0]
            self.add_npc(npc_type(self.game, pos=(x + 0.5, y + 0.5)))
            spawned += 1

        # If we couldn't spawn all enemies, log a warning
        if spawned < count:
            print(f"Warning: Could only spawn {spawned} of {count} enemies due to map constraints")

    def reset(self):
        """Reset the object handler for a new level"""
        # Clear all sprites and NPCs
        self.sprite_list = []
        self.npc_list = []
        self.npc_positions = {}
        self.win_message_shown = False

        # Spawn NPCs for the new level
        self.spawn_npc()

        # Load decorative sprites for the new level
        self.load_decorative_sprites()