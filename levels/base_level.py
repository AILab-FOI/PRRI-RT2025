"""
Base level module with common functions and structures for all levels
"""
# No imports needed for the base structure

def create_base_level_structure():
    """
    Create a base level structure with common fields
    that all levels should have
    """
    return {
        'narrative': {
            'intro': "",
            'objective': "",
            'conclusion': ""
        },
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
