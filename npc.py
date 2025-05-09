"""
NPC module - imports from the npcs package for backward compatibility.
"""

# Import all NPC classes from the npcs package
from npcs import (
    NPC,
    StaticNPC,
    DialogueNPC,
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
