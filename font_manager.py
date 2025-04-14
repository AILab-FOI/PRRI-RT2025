import pygame as pg

def load_custom_font(size, bold=False):
    """
    Load the custom game font with fallback to system font
    
    Args:
        size (int): Font size
        bold (bool): Whether the font should be bold (only applies to fallback font)
        
    Returns:
        pygame.font.Font: The loaded font
    """
    try:
        return pg.font.Font('resources/fonts/kenvector_future.ttf', size)
    except:
        # Fallback to system font if custom font fails to load
        return pg.font.SysFont('Arial', size, bold=bold)
