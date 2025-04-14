from sprite_object import *
from npc import *
from random import choices, randrange


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

        # Load enemy configuration from level manager
        self.load_enemy_config()

        # Spawn enemies based on level configuration
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

    def load_enemy_config(self):
        """Load enemy configuration from level manager"""
        enemy_config = self.game.level_manager.get_enemy_config()
        self.enemies = enemy_config['count']
        self.npc_types = enemy_config['types']
        self.weights = enemy_config['weights']
        self.restricted_area = enemy_config['restricted_area']

    def spawn_npc(self):
        """Spawn NPCs based on the current level configuration"""
        # Clear existing NPCs
        self.npc_list = []
        self.npc_positions = {}
        self.win_message_shown = False

        # Spawn new NPCs according to configuration
        for _ in range(self.enemies):
            npc = choices(self.npc_types, self.weights)[0]
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        # Check if all enemies are defeated
        self.all_enemies_defeated = not len(self.npc_positions)

        # If all enemies are defeated, show a message and enable the level exit door
        if self.all_enemies_defeated and not self.win_message_shown:
            self.win_message_shown = True
            self.game.object_renderer.show_message(f"All {self.enemies} enemies defeated! Find the exit door.")
            # Enable the level exit door
            self.enable_level_exit()

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
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

    def reset(self):
        """Reset the object handler for a new level"""
        # Keep static sprites but clear NPCs
        self.npc_list = []
        self.npc_positions = {}
        self.win_message_shown = False

        # Load new enemy configuration and spawn NPCs
        self.load_enemy_config()
        self.spawn_npc()