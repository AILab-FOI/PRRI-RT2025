from sprite_object import *
from npc import *
from random import choices


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        self.npc_positions = {}
        self.win_message_shown = False

        # Spawn enemies based on level configuration
        # This will also load the enemy configuration from level manager
        self.spawn_npc()

        # sprite map
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(12.9, 33.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(12.2, 33.5)))

        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(1.5, 26.1)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.9, 26.1)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(2.3, 26.1)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.1, 26.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.1, 27)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.1, 27.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(1.1, 28)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(1.1, 28.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(1.1, 29)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.1, 29.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.1, 30)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.1, 30.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.1, 31)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(1.1, 31.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(1.1, 32)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(1.1, 32.5)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(1.5, 32.9)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(1.9, 32.9)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(2.3, 32.9)))

        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(23.2, 31.2)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(23.2, 33.5)))

        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(20.2, 31.8)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(15.2, 32.3)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(8.9, 32.3)))

        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(20.2, 12.2)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(20.2, 13.2)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras1.png', pos=(20.2, 14.2)))

        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(20.2, 12.7)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(20.2, 13.7)))
        add_sprite(SpriteObject(game, path=self.static_sprite_path + 'ukras2.png', pos=(20.2, 14.7)))
        # add_sprite(SpriteObject(game, path=self.static_sprite_path + 'konzola.jpg', pos=(2, 14.5)))

        """
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 5.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(3.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))
        """
        # npc map
        # add_npc(SoldierNPC(game, pos=(11.0, 19.0)))
        # add_npc(SoldierNPC(game, pos=(11.5, 4.5)))
        # add_npc(SoldierNPC(game, pos=(13.5, 6.5)))
        # add_npc(SoldierNPC(game, pos=(2.0, 20.0)))
        # add_npc(SoldierNPC(game, pos=(4.0, 29.0)))
        # add_npc(CacoDemonNPC(game, pos=(5.5, 14.5)))
        # add_npc(CacoDemonNPC(game, pos=(5.5, 16.5)))
        # add_npc(CyberDemonNPC(game, pos=(14.5, 25.5)))

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
        # Keep static sprites but clear NPCs
        self.npc_list = []
        self.npc_positions = {}
        self.win_message_shown = False

        # Spawn NPCs for the new level
        self.spawn_npc()