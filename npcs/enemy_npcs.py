"""
Enemy NPC classes for the game.
"""

import pygame as pg
import os
from collections import deque
from random import random
from settings import *
from npcs.base_npc import NPC


class KlonoviNPC(NPC):
    """Klonovi enemy type"""
    def __init__(self, game, path='resources/sprites/npc/klonovi/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.original_height_shift = self.SPRITE_HEIGHT_SHIFT
        self.death_height_shift = 0.7


class StakorNPC(NPC):
    """Stakor (rat) enemy type"""
    def __init__(self, game, path='resources/sprites/npc/stakor/0.png', pos=(10.5, 5.5),
                 scale=0.5, shift=0.4, animation_time=200):
        super().__init__(game, path, pos, scale, shift, animation_time)

        self.death_images = deque()
        death_path = self.path + '/death'
        for file_name in ['0.png', '1.png']:
            if os.path.isfile(os.path.join(death_path, file_name)):
                img = pg.image.load(death_path + '/' + file_name).convert_alpha()
                self.death_images.append(img)
        # Death height shift will be applied when enemy dies
        self.death_height_shift = 0.8

        self.walk_images = self.get_images(self.path + '/walk')

        # Karakteristike štakora
        self.attack_dist = 1.0     # udaljenost napada
        self.health = 50           # zdravlje
        self.attack_damage = 5     # Srednji damage za melee napad
        self.speed = 0.05          # Brzina
        self.accuracy = 0.3        # točnost za melee napad

    # Napad štakora
    def attack(self):
        if self.animation_trigger:
            self.game.sound.napad_stakor.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    # Smrt štakora
    def check_health(self):
        if self.health < 1 and self.alive:
            self.game.sound.stakor_smrt.play()
            super().check_health()


class TosterNPC(NPC):
    """Toster enemy type"""
    def __init__(self, game, path='resources/sprites/npc/toster/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.4, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Death height shift will be applied when enemy dies
        self.death_height_shift = 0.7

        # Karakteristike tostera
        self.attack_dist = 4.0     # udaljenost napada (ranged)
        self.health = 80           # zdravlje
        self.attack_damage = 8     # Medium damage
        self.speed = 0.03          # Srednja brzina
        self.accuracy = 0.25       # točnost za ranged napad

    # Napad tostera
    def attack(self):
        if self.animation_trigger:
            self.game.sound.toster_attack.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    # Smrt tostera
    def check_health(self):
        if self.health < 1 and self.alive:
            self.game.sound.toster_death.play()
            super().check_health()

    # Damage tostera
    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.toster_damage.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()


class ParazitNPC(NPC):
    """Parazit enemy type - mini-boss in level 3"""
    def __init__(self, game, path='resources/sprites/npc/parazit/0.png', pos=(10.5, 5.5),
                 scale=0.8, shift=0.4, animation_time=200):  # Increased scale to make it larger
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Death height shift will be applied when enemy dies
        self.death_height_shift = 0.8

        # Karakteristike parazita (enhanced for mini-boss role)
        self.attack_dist = 2.0     # udaljenost napada (melee) - increased range
        self.health = 200          # zdravlje - significantly increased for mini-boss
        self.attack_damage = 15    # High damage - increased
        self.speed = 0.05          # Fast but slightly slower than before
        self.accuracy = 0.4        # točnost za melee napad - increased

    # Napad parazita
    def attack(self):
        if self.animation_trigger:
            self.game.sound.parazit_attack.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    # Smrt parazita
    def check_health(self):
        if self.health < 1 and self.alive:
            self.game.sound.parazit_death.play()
            super().check_health()

    # Damage parazita
    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.parazit_damage.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()


class JazavacNPC(NPC):
    """Jazavac enemy type"""
    def __init__(self, game, path='resources/sprites/npc/jazavac/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Death height shift will be applied when enemy dies
        self.death_height_shift = 0.7

        # Karakteristike jazavca
        self.attack_dist = 2.5     # udaljenost napada (medium range)
        self.health = 120          # zdravlje (high)
        self.attack_damage = 15    # High damage
        self.speed = 0.025         # Slow
        self.accuracy = 0.3        # točnost za napad

    # Napad jazavca
    def attack(self):
        if self.animation_trigger:
            self.game.sound.jazavac_attack.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    # Smrt jazavca
    def check_health(self):
        if self.health < 1 and self.alive:
            self.game.sound.jazavac_death.play()
            super().check_health()

    # Damage jazavca
    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.jazavac_damage.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()


class MadracNPC(NPC):
    """Madrac enemy type"""
    def __init__(self, game, path='resources/sprites/npc/madraci/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.4, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # Death height shift will be applied when enemy dies
        self.death_height_shift = 0.7

        # Karakteristike madraca
        self.attack_dist = 3.0     # udaljenost napada (medium range)
        self.health = 90           # zdravlje (medium-high)
        self.attack_damage = 12    # Medium-high damage
        self.speed = 0.04          # Medium-fast speed
        self.accuracy = 0.35       # točnost za napad

    # Napad madraca
    def attack(self):
        if self.animation_trigger:
            self.game.sound.madrac_attack.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    # Smrt madraca
    def check_health(self):
        if self.health < 1 and self.alive:
            self.game.sound.madrac_death.play()
            super().check_health()

    # Damage madraca
    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:
                self.game.sound.madrac_damage.play()
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()
