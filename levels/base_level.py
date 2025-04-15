"""
Base level module with common functions and structures for all levels
"""
from npc import KlonoviNPC, StakorNPC

def create_base_level_structure():
    """
    Create a base level structure with common fields
    that all levels should have
    """
    return {
        'terminals': [],
        'doors': [],
        'weapons': [],
        'powerups': [],
        'sprites': [],
        'dialogue_npcs': [],
        'enemies': {
            'count': 0,
            'types': [],
            'weights': [],
            'restricted_area': set(),
            'fixed_positions': []
        }
    }
