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
        config = {
            'attack_dist': 4,
            'health': 70,
            'attack_damage': 5,
            'speed': 0.04,
            'accuracy': 0.25,
            'death_height_shift': 0.7,
            'behavior': 'ranged',
            'sounds': {
                'attack': 'npc_attack',
                'pain': 'npc_pain',
                'death': 'npc_death'
            }
        }
        super().__init__(game, path, pos, scale, shift, animation_time, config)
        self.original_height_shift = self.SPRITE_HEIGHT_SHIFT


class StakorNPC(NPC):
    """Stakor (rat) enemy type"""
    def __init__(self, game, path='resources/sprites/npc/stakor/0.png', pos=(10.5, 5.5),
                 scale=0.5, shift=0.4, animation_time=200):
        config = {
            'attack_dist': 1.5,
            'health': 50,
            'attack_damage': 6,
            'speed': 0.035,
            'accuracy': 0.3,
            'death_height_shift': 0.8,
            'behavior': 'melee',
            'sounds': {
                'attack': 'stakor_napad',
                'pain': 'npc_pain',
                'death': 'stakor_smrt'
            }
        }
        super().__init__(game, path, pos, scale, shift, animation_time, config)

        self.death_images = deque()
        death_path = self.path + '/death'
        for file_name in ['0.png', '1.png']:
            if os.path.isfile(os.path.join(death_path, file_name)):
                img = pg.image.load(death_path + '/' + file_name).convert_alpha()
                self.death_images.append(img)
        self.walk_images = self.get_images(self.path + '/walk')


class TosterNPC(NPC):
    """Toster enemy type"""
    def __init__(self, game, path='resources/sprites/npc/toster/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.4, animation_time=180):
        config = {
            'attack_dist': 4.0,
            'health': 80,
            'attack_damage': 7,
            'speed': 0.035,
            'accuracy': 0.3,
            'death_height_shift': 0.7,
            'behavior': 'ranged',
            'sounds': {
                'attack': 'toster_attack',
                'pain': 'toster_damage',
                'death': 'toster_death'
            }
        }
        super().__init__(game, path, pos, scale, shift, animation_time, config)


class ParazitNPC(NPC):
    """Parazit enemy type - mini-boss in level 3"""
    def __init__(self, game, path='resources/sprites/npc/parazit/0.png', pos=(10.5, 5.5),
                 scale=0.8, shift=0.4, animation_time=200):
        config = {
            'attack_dist': 2.0,
            'health': 450,
            'attack_damage': 15,
            'speed': 0.05,
            'accuracy': 0.4,
            'death_height_shift': 0.8,
            'behavior': 'melee',
            'sounds': {
                'attack': 'parazit_attack',
                'pain': 'parazit_damage',
                'death': 'parazit_death'
            }
        }
        super().__init__(game, path, pos, scale, shift, animation_time, config)


class JazavacNPC(NPC):
    """Jazavac enemy type"""
    def __init__(self, game, path='resources/sprites/npc/jazavac/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        config = {
            'attack_dist': 2.0,
            'health': 120,
            'attack_damage': 12,
            'speed': 0.025,
            'accuracy': 0.3,
            'death_height_shift': 0.7,
            'behavior': 'melee',
            'sounds': {
                'attack': 'jazavac_attack',
                'pain': 'jazavac_damage',
                'death': 'jazavac_death'
            }
        }
        super().__init__(game, path, pos, scale, shift, animation_time, config)


class MadracNPC(NPC):
    """Madrac enemy type"""
    def __init__(self, game, path='resources/sprites/npc/madraci/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.4, animation_time=180):
        config = {
            'attack_dist': 1.5,
            'health': 200,
            'attack_damage': 10,
            'speed': 0.03,
            'accuracy': 0.3,
            'death_height_shift': 0.7,
            'behavior': 'ranged',
            'sounds': {
                'attack': 'madrac_attack',
                'pain': 'madrac_damage',
                'death': 'madrac_death'
            }
        }
        super().__init__(game, path, pos, scale, shift, animation_time, config)


class BossNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/boss/0.png', pos=(10.5, 5.5),
                 scale=1.5, shift=0, animation_time=220):
        config = {
            'attack_dist': 3.5,
            'health': 800,
            'attack_damage': 20,
            'speed': 0.06,
            'accuracy': 0.45,
            'death_height_shift': 0.3,
            'behavior': 'melee',
            'sounds': {
                'attack': 'boss_attack',
                'pain': 'boss_damage',
                'death': 'boss_death'
            }
        }
        super().__init__(game, path, pos, scale, shift, animation_time, config)
