import math

# game settings
RES = WIDTH, HEIGHT = 1600, 900
# RES = WIDTH, HEIGHT = 1920, 1080
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 0

# Default player positions for each level
PLAYER_POS = 1.5, 2.5  # Level 1 starting position
PLAYER_POS_LEVEL2 = 12.5, 2.5  # Level 2 starting position
PLAYER_POS_LEVEL3 = 12.5, 2.5  # Level 3 starting position
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100

# dash settings
PLAYER_DASH_MULTIPLIER = 3.0  # koliko je dash brži od normalnog kretanja
PLAYER_DASH_DURATION = 200    # trajanje dasha u milisekundama
PLAYER_DASH_COOLDOWN = 1000   # cooldown dasha u milisekundama

MOUSE_SENSITIVITY = 0.0003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FLOOR_COLOR = (30, 30, 30)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2

# UI settings
LOADING_BACKGROUND_IMAGE = 'resources/textures/sky.png'  # Path to the loading screen background image
LOADING_DURATION = 2000  # Minimum loading time in milliseconds
LOADING_FADE_DURATION = 500  # Fade transition duration in milliseconds
LOADING_TIP_CHANGE_INTERVAL = 3000  # Time between tip changes in milliseconds
LOADING_PARTICLE_COUNT = 30  # Number of background particles