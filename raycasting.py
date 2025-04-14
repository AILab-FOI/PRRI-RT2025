import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures
        # Precompute some values
        self.wall_column_cache = {}  # Cache for scaled wall columns

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            # Create a cache key for this wall column
            cache_key = (texture, offset, proj_height)

            # Check if we have this wall column in cache
            if cache_key in self.wall_column_cache:
                wall_column, wall_pos = self.wall_column_cache[cache_key]
                # Adjust wall position for the current ray
                wall_pos = (ray * SCALE, wall_pos[1])
            else:
                # Calculate wall column and position
                if proj_height < HEIGHT:
                    wall_column = self.textures[texture].subsurface(
                        offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                    )
                    wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                    wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
                else:
                    texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                    wall_column = self.textures[texture].subsurface(
                        offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                        SCALE, texture_height
                    )
                    wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                    wall_pos = (ray * SCALE, 0)

                # Store in cache (with a generic x position)
                self.wall_column_cache[cache_key] = (wall_column, (0, wall_pos[1]))

                # Limit cache size to prevent memory issues
                if len(self.wall_column_cache) > 1000:
                    # Clear oldest 20% of cache when it gets too large
                    keys_to_remove = list(self.wall_column_cache.keys())[:200]
                    for key in keys_to_remove:
                        del self.wall_column_cache[key]

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        world_map = self.game.map.world_map  # Local reference for faster access

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001

        # Precompute sin and cos values for all rays
        sin_angles = [math.sin(ray_angle + i * DELTA_ANGLE) for i in range(NUM_RAYS)]
        cos_angles = [math.cos(ray_angle + i * DELTA_ANGLE) for i in range(NUM_RAYS)]

        for ray in range(NUM_RAYS):
            sin_a = sin_angles[ray]
            cos_a = cos_angles[ray]

            # Avoid division by zero
            sin_a = 0.000001 if abs(sin_a) < 0.000001 else sin_a
            cos_a = 0.000001 if abs(cos_a) < 0.000001 else cos_a

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            texture_hor = None
            for _ in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in world_map:
                    texture_hor = world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            if texture_hor is None:
                # If no wall was hit, set a very large depth
                depth_hor = float('inf')

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            texture_vert = None
            for _ in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in world_map:
                    texture_vert = world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if texture_vert is None:
                # If no wall was hit, set a very large depth
                depth_vert = float('inf')

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - (ray_angle + ray * DELTA_ANGLE))

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()

    def clear_cache(self):
        """Clear the wall column cache to free memory"""
        self.wall_column_cache.clear()