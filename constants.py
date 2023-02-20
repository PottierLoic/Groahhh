"""
Constants.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Window size.
WIDTH = 800
HEIGHT = 800

# Quadtree.
CAPACITY = 1

# Colors. (to remove when sprites are implemented)
BACKGROUND_COLOR = "light grey"

# Sizes. (to remove when sprites are implemented)
PLAYER_HITBOX = 25
ZOMBIE_SIZE = 50
BULLET_SIZE = 2
DIAMOND_SIZE = 12
CHEST_SIZE = 15
FIREBALL_SIZE = 16

# Animation speed.
ANIMATION_SPEED = 30

# Refresh rate.
DELAY = 1

# Basic bullet stats.
FALL_DISTANCE = 200
BULLET_SPEED = 1
WEAPON_DELAY = 100

# Fireball stats.
FALL_DISTANCE_FIREBALL = 400
FIREBALL_SPEED = 1
FIREBALL_DELAY = 1000

# Spawn stats.
SPAWN_DELAY = 100
SPAWN_RANGE = 400
SAFE_DISTANCE = 200
DIAMOND_SPAWN_CHANCE = 10
CHEST_SPAWN_CHANCE = 20
ROUND_DELAY = 1000

# Basic zombie stats.
ZOMBIE_SPEED = 3
HIT_DELAY = 100

# Player level amount.
EXPERIENCE_AMOUNT = [40, 60, 100, 150, 210, 280, 700, 800, 900, 100000]

# Rounds stats.
ROUNDS_SPAWNS = [20, 40, 60, 100, 150]

# Chests
REWARD_POOL = ["orb", "wand", "aura", "fireball", "meteor"]

# Orb stats.
ORB_REVOLUTION_RADIUS = 80
ORB_RADIUS = 30
