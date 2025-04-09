from sprite_object import *
from random import randint, random


class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 20
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.death_frame = 0  # Use a consistent name for death animation frame counter
        self.player_search_trigger = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        # self.draw_ray_cast()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        # pg.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_attack.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def animate_death(self):
        if not self.alive and len(self.death_images) > 0:
            # Use animation_trigger for smoother animation
            if self.animation_trigger and self.death_frame < len(self.death_images) - 1:
                # Increment the death frame counter, but only if we haven't reached the last frame
                self.death_frame += 1
                # Set the image to the current death frame
                self.image = self.death_images[self.death_frame]

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1 and self.alive:  # Check if the enemy is already dead
            self.alive = False

            if type(self) is NPC:
                self.game.sound.npc_death.play()

            # Reset death frame counter and set the initial death frame immediately
            self.death_frame = 0

            if hasattr(self, 'death_height_shift'):
                self.SPRITE_HEIGHT_SHIFT = self.death_height_shift
            else:
                self.SPRITE_HEIGHT_SHIFT = 0.5  # Default value
            if len(self.death_images) > 0:
                self.image = self.death_images[0]

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        EPSILON = 1e-6
        sin_a = sin_a if abs(sin_a) > EPSILON else EPSILON * (1 if sin_a >= 0 else -1)
        cos_a = cos_a if abs(cos_a) > EPSILON else EPSILON * (1 if cos_a >= 0 else -1)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for _ in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for _ in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    # Debug method for visualizing ray casting - not used in production
    # def draw_ray_cast(self):
    #     pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
    #     if self.ray_cast_player_npc():
    #         pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
    #                      (100 * self.x, 100 * self.y), 2)

'''
class SoldierNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)


class CacoDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/caco_demon/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35

class CyberDemonNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/cyber_demon/0.png', pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25
'''
class KlonoviNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/klonovi/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        # No need to reload death images as they're already loaded in the parent class
        # Store original height shift for restoration when needed
        self.original_height_shift = self.SPRITE_HEIGHT_SHIFT
        # Set death height shift (will be applied when enemy dies)
        self.death_height_shift = 0.7  # Specific value for KlonoviNPC

class StakorNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/stakor/0.png', pos=(10.5, 5.5),
                 scale=0.5, shift=0.4, animation_time=200):
        super().__init__(game, path, pos, scale, shift, animation_time)
        # Posebno učitamo slike za smrt jer imamo drugačiju strukturu direktorija
        self.death_images = deque()
        death_path = self.path + '/death'
        for file_name in ['0.png', '1.png']:
            if os.path.isfile(os.path.join(death_path, file_name)):
                img = pg.image.load(death_path + '/' + file_name).convert_alpha()
                self.death_images.append(img)
        # Death height shift will be applied when enemy dies
        self.death_height_shift = 0.8
        # Koristimo walk slike za hodanje
        self.walk_images = self.get_images(self.path + '/walk')

        # Karakteristike štakora
        self.attack_dist = 1.0     # udaljenost napada
        self.health = 50           # zdravlje
        self.attack_damage = 5     # Srednji damage za melee napad
        self.speed = 0.05          # Brzina
        self.accuracy = 0.3        # točnost za melee napad

    #Napad štakora
    def attack(self):
        if self.animation_trigger:
            self.game.sound.napad_stakor.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)
    def check_health(self):
        if self.health < 1 and self.alive:
            # Play the custom sound for this NPC type
            self.game.sound.stakor_smrt.play()
            # Call parent method with alive still set to True
            super().check_health()
