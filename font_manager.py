import pygame as pg

def load_custom_font(size, bold=False):
    try:
        return pg.font.Font('resources/fonts/kenvector_future.ttf', size)
    except:
        # Fallback to system font if custom font fails to load
        return pg.font.SysFont('Arial', size, bold=bold)
