"""
NPC package for the game.
"""

from npcs.base_npc import NPC, StaticNPC
from npcs.dialogue_npc import DialogueNPC
from npcs.enemy_npcs import (
    KlonoviNPC,
    StakorNPC,
    TosterNPC,
    ParazitNPC,
    JazavacNPC,
    MadracNPC,
    BossNPC
)
from npcs.npc_factory import NPCFactory

__all__ = [
    'NPC',
    'StaticNPC',
    'DialogueNPC',
    'KlonoviNPC',
    'StakorNPC',
    'TosterNPC',
    'ParazitNPC',
    'JazavacNPC',
    'MadracNPC',
    'NPCFactory',
    'BossNPC'
]
