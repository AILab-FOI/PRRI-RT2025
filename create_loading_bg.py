import pygame as pg
import os
import math

# Initialize pygame
pg.init()

# Define dimensions
WIDTH, HEIGHT = 1600, 900
screen = pg.Surface((WIDTH, HEIGHT))

# Fill background with dark color
screen.fill((20, 20, 30))

# Create a gradient effect
for i in range(100):
    alpha = 100 - i
    gradient = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    gradient.fill((0, 0, 0, alpha))
    screen.blit(gradient, (0, i * HEIGHT // 100))

# Add some decorative elements
for i in range(20):
    x = i * 80
    y = HEIGHT // 2 + 100 * math.sin(i * 0.3)
    radius = 5 + i % 10
    pg.draw.circle(screen, (50, 100, 150, 100), (x, int(y)), radius)

# Add a title
font = pg.font.SysFont('Arial', 72, bold=True)
title = font.render("PRRI-RT2025", True, (200, 200, 220))
title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
screen.blit(title, title_rect)

# Make sure the directory exists
os.makedirs('resources/textures', exist_ok=True)

# Save the image
pg.image.save(screen, 'resources/textures/loading_bg.png')

print("Loading background created at resources/textures/loading_bg.png")
