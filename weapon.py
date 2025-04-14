from sprite_object import *


class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/pistol/0.png', scale=0.4, animation_time=90, damage=50, name='pistol'):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = damage
        self.name = name

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()


class SMG(Weapon):
    def __init__(self, game):
        # SMG has faster animation time (40 vs 90) and lower damage (15 vs 50)
        # Animation time is very fast to support automatic firing
        super().__init__(game=game,
                         path='resources/sprites/weapon/smg/0.png',
                         scale=0.5,  # Slightly larger than original but smaller than pistol
                         animation_time=40,
                         damage=15,
                         name='smg')

        # Override the weapon position to move it more to the right
        # Calculate new position based on the image size
        right_offset = 100  # Same offset as pistol for consistency
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2 + right_offset,
                          HEIGHT - self.images[0].get_height())

        # Play SMG sound instead of pistol sound when firing
        # Note: You'll need to add this sound to the Sound class


class Pistol(Weapon):
    def __init__(self, game):
        # Larger scale (0.6 instead of 0.4) for the pistol
        super().__init__(game=game,
                         path='resources/sprites/weapon/pistol/0.png',
                         scale=1.2,  # Increased from 0.4
                         animation_time=90,
                         damage=50,
                         name='pistol')

        # Override the weapon position to move it more to the right
        # Calculate new position based on the image size
        right_offset = 230  # Pixels to move right
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2 + right_offset,
                          HEIGHT - self.images[0].get_height())