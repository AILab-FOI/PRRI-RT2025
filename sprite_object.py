import pygame as pg
from settings import *
import os
from collections import deque


class SpriteObject:
    def __init__(self, game, path=None,
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        # Use a more neutral default or no default at all
        if path is None:
            path = 'resources/sprites/static_sprites/ukras1.png'
        self.game = game
        self.player = game.player
        self.x, self.y = pos

        # Add error handling for missing textures
        try:
            if os.path.isfile(path):
                self.image = pg.image.load(path).convert_alpha()
            else:
                print(f"Warning: Sprite texture not found at {path}")
                # Create a small blank/transparent surface instead
                self.image = pg.Surface((32, 32), pg.SRCALPHA)
                self.image.fill((0, 0, 0, 0))  # Transparent
        except Exception as e:
            print(f"Error loading sprite texture: {e}")
            # Create a small blank/transparent surface
            self.image = pg.Surface((32, 32), pg.SRCALPHA)
            self.image.fill((0, 0, 0, 0))  # Transparent
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # Round the dimensions to reduce the number of unique scaled images
        proj_width = round(proj_width)
        proj_height = round(proj_height)

        # We'll use a simple caching mechanism based on the dimensions
        cache_key = (proj_width, proj_height)

        # Create the cache attribute if it doesn't exist
        if not hasattr(self, '_scaled_image_cache'):
            self._scaled_image_cache = {}

        # Get the scaled image from cache or create a new one
        if cache_key not in self._scaled_image_cache:
            self._scaled_image_cache[cache_key] = pg.transform.scale(self.image, (proj_width, proj_height))

            # Limit cache size to prevent memory issues (keep only the 10 most recent sizes)
            if len(self._scaled_image_cache) > 10:
                # Remove the oldest entry
                oldest_key = next(iter(self._scaled_image_cache))
                del self._scaled_image_cache[oldest_key]

        image = self._scaled_image_cache[cache_key]

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        try:
            if os.path.isdir(path):
                for file_name in os.listdir(path):
                    if os.path.isfile(os.path.join(path, file_name)):
                        try:
                            img = pg.image.load(path + '/' + file_name).convert_alpha()
                            images.append(img)
                        except Exception as e:
                            print(f"Error loading animation frame {file_name}: {e}")
            else:
                print(f"Warning: Animation directory not found at {path}")
                # Create a blank image if directory doesn't exist
                blank_img = pg.Surface((32, 32), pg.SRCALPHA)
                blank_img.fill((0, 0, 0, 0))  # Transparent
                images.append(blank_img)
        except Exception as e:
            print(f"Error loading animation frames: {e}")
            # Create a blank image if there's an error
            blank_img = pg.Surface((32, 32), pg.SRCALPHA)
            blank_img.fill((0, 0, 0, 0))  # Transparent
            images.append(blank_img)

        # Make sure we have at least one image
        if not images:
            blank_img = pg.Surface((32, 32), pg.SRCALPHA)
            blank_img.fill((0, 0, 0, 0))  # Transparent
            images.append(blank_img)

        return images
