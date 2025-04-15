from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()

        # Dash svojstva
        self.is_dashing = False
        self.dash_direction = (0, 0)
        self.dash_start_time = 0
        self.last_dash_time = 0

        # Dialogue mode - when active, player can't move
        self.dialogue_mode = False

        # Automatic weapon firing properties
        self.auto_fire = False 
        self.auto_fire_delay = 150 
        self.last_auto_fire_time = 0 

        # Invulnerability powerup properties
        self.is_invulnerable = False
        self.invulnerability_start_time = 0
        self.invulnerability_time_left = 0

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        if self.health < 1:
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):
        if self.is_invulnerable:
            return

        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.igrac_damage.play()
        self.check_game_over()

    def single_fire_event(self, event):

        if self.dialogue_mode:
            return

        # Handle mouse button down - start firing
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                # For SMG, start auto-firing mode
                if self.game.weapon.name == 'smg':
                    self.auto_fire = True
                    self.fire_weapon()
                else:  # For pistol, just fire once
                    self.fire_weapon()

        # Handle mouse button up - stop auto-firing
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.auto_fire = False

    def fire_weapon(self):
        # Play the appropriate sound based on weapon type
        if self.game.weapon.name == 'smg':
            self.game.sound.smg.play()
        else: 
            self.game.sound.pistolj.play()
        self.shot = True
        self.game.weapon.reloading = True
        self.last_auto_fire_time = pg.time.get_ticks()

    def movement(self):
        if self.dialogue_mode:
            return

        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        # Spremi normalizirani smjer kretanja za dash
        if dx != 0 or dy != 0:
            length = math.sqrt(dx * dx + dy * dy)
            self.dash_direction = (dx / length, dy / length)
        else:
            self.dash_direction = (cos_a, sin_a)

        if keys[pg.K_SPACE] and not self.is_dashing:
            self.dash()

        self.check_wall_collision(dx, dy)
        self.angle %= math.tau

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_control(self):
        if self.dialogue_mode:
            return

        mx, _ = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def dash(self):
        # Provjeri je li dash na cooldownu
        current_time = pg.time.get_ticks()
        if current_time - self.last_dash_time < PLAYER_DASH_COOLDOWN:
            return False

        # Provjeri ima li smjer kretanja
        if self.dash_direction == (0, 0):
            return False

        # Započni dash
        self.is_dashing = True
        self.dash_start_time = current_time
        self.last_dash_time = current_time

        self.game.sound.player_dash.play()
        return True

    def update_dash(self):
        if not self.is_dashing:
            return

        current_time = pg.time.get_ticks()
        # Provjeri je li dash završio
        if current_time - self.dash_start_time > PLAYER_DASH_DURATION:
            self.is_dashing = False
            return

        # Primijeni dash kretanje
        dx, dy = self.dash_direction
        dash_speed = PLAYER_SPEED * PLAYER_DASH_MULTIPLIER * self.game.delta_time
        self.check_wall_collision(dx * dash_speed, dy * dash_speed)

    def activate_invulnerability(self):
        """Activate invulnerability powerup"""
        self.is_invulnerable = True
        self.invulnerability_start_time = pg.time.get_ticks()
        self.invulnerability_time_left = POWERUP_INVULNERABILITY_DURATION
        self.game.sound.powerup_pickup.play()
        self.game.sound.powerup_active.play(-1)

    def update_invulnerability(self):
        """Update invulnerability state"""
        if not self.is_invulnerable:
            return

        current_time = pg.time.get_ticks()
        elapsed = current_time - self.invulnerability_start_time

        # Calculate time left in seconds (rounded up)
        self.invulnerability_time_left = max(0, POWERUP_INVULNERABILITY_DURATION - elapsed)

        # Check if invulnerability has expired
        if self.invulnerability_time_left <= 0:
            self.is_invulnerable = False
            # Stop the active sound
            self.game.sound.powerup_active.stop()
            # Play the end sound
            self.game.sound.powerup_end.play()

    def update(self):
        if not self.is_dashing:
            self.movement()
        self.update_dash()
        self.update_invulnerability()
        self.mouse_control()
        self.recover_health()
        self.update_auto_fire()

    def update_auto_fire(self):
        # Handle automatic firing for SMG
        if self.auto_fire and self.game.weapon.name == 'smg':
            current_time = pg.time.get_ticks()
            # Check if enough time has passed since the last shot
            if (not self.game.weapon.reloading and
                current_time - self.last_auto_fire_time >= self.auto_fire_delay):
                self.fire_weapon()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)