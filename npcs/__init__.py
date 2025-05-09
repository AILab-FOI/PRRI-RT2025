"""
NPC package for the game.
This package contains all NPC-related classes.
"""

from npcs.base_npc import NPC, StaticNPC
from npcs.dialogue_npc import DialogueNPC
from npcs.enemy_npcs import (
    KlonoviNPC,
    StakorNPC,
    TosterNPC,
    ParazitNPC,
    JazavacNPC,
    MadracNPC
)

# For backwards compatibility
__all__ = [
    'NPC',
    'StaticNPC',
    'DialogueNPC',
    'KlonoviNPC',
    'StakorNPC',
    'TosterNPC',
    'ParazitNPC',
    'JazavacNPC',
    'MadracNPC'
]
