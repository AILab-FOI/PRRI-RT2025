import pygame as pg
import math
from settings import *
from sprite_object import SpriteObject


class PowerUp(SpriteObject):
    def __init__(self, game, path='resources/teksture/level1/powerup.png', pos=(10.5, 3.5), powerup_type='invulnerability'):

        # Add 0.5 to position for proper sprite rendering in the center of the tile
        adjusted_pos = (pos[0] + 0.5, pos[1] + 0.5) if isinstance(pos, tuple) else pos

        super().__init__(game, path, adjusted_pos, scale=0.35, shift=1)

        self.powerup_type = powerup_type
        self.pickup_distance = POWERUP_PICKUP_DISTANCE
        self.collected = False

    def update(self):
        super().update()

        # Check if player is close enough to pick up the powerup
        if not self.collected:
            player_pos = self.game.player.pos
            distance = math.hypot(player_pos[0] - self.x, player_pos[1] - self.y)

            if distance < self.pickup_distance:
                self.collect()

    def collect(self):
        """Player collects the powerup"""
        if self.collected:
            return

        self.collected = True

        # Apply powerup effect based on type
        if self.powerup_type == 'invulnerability':
            self.game.player.activate_invulnerability()

        # Remove the powerup from the game
        if self in self.game.object_handler.sprite_list:
            self.game.object_handler.sprite_list.remove(self)
