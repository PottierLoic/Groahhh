"""
Constants.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Window size.
WIDTH = 600
HEIGHT = 600

# Quadtree.
CAPACITY = 4
DRAW_RECT = True

# Colors. (to remove when sprites are implemented)
BACKGROUND_COLOR = "light grey"

# Sizes. (to remove when sprites are implemented)
PLAYER_HITBOX = 25
ZOMBIE_SIZE = 24
BULLET_SIZE = 2
DIAMOND_SIZE = 12
CHEST_SIZE = 15

# Animation speed.
ANIMATION_SPEED = 30

# Refresh rate.
DELAY = 1

# Basic bullet stats.
FALL_DISTANCE = 200
BULLET_SPEED = 2

# Basic weapon stats.
WEAPON_DELAY = 100

# Spawn stats.
SPAWN_DELAY = 100
SPAWN_RANGE = 400
SAFE_DISTANCE = 200
DIAMOND_SPAWN_CHANCE = 50
CHEST_SPAWN_CHANCE = 20

# Basic zombie stats.
ZOMBIE_SPEED = 5
HIT_DELAY = 100

# Player level amount.
EXPERIENCE_AMOUNT = [100, 200, 300, 400, 500, 600, 700, 800, 900, 100000]

# Rounds stats.
ROUNDS_SPAWNS = [20, 40, 60, 100, 150]

# Chests
REWARD_POOL = ["orb", "wand", "aura", "laser", "meteor"]

# Orb stats.
ORB_REVOLUTION_RADIUS = 80
ORB_RADIUS = 20
