"""
Constants.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Window size.
WIDTH = 400
HEIGHT = 400

# Quadtree.
CAPACITY = 1

# Colors. (to remove when sprites are implemented)
BACKGROUND_COLOR = "light grey"

# Sizes.
PLAYER_HITBOX = 25
ZOMBIE_SIZE = 50
BULLET_SIZE = 2
DIAMOND_SIZE = 12
CHEST_SIZE = 15
FIREBALL_SIZE = 16
METEOR_SIZE = 80

# Animation speed.
ORB_ANIMATION_SPEED = 10
AURA_ANIMATION_SPEED = 2
METEOR_ANIMATION_SPEED = 10
ANIMATION_SPEED = 30

# ENGINE
PHYSICS_REFRESH_RATE = 1/120
FRAME_RATE = 1/60

# Refresh rate.
DELAY = 1

# Basic bullet stats.
FALL_DISTANCE = 200
BULLET_SPEED = 2
WEAPON_DELAY = 100

# Fireball stats.
FALL_DISTANCE_FIREBALL = 400
FIREBALL_SPEED = 1
FIREBALL_DELAY = 1000

# Meteors stats.
METEOR_DELAY = 100

# Spawn stats.
SPAWN_DELAY = 10
SPAWN_RANGE = 300
SAFE_DISTANCE = 200
DIAMOND_SPAWN_CHANCE = 30
CHEST_SPAWN_CHANCE = 20
ROUND_DELAY = 1000

# Basic zombie stats.
ZOMBIE_SPEED = 15
HIT_DELAY = 100

# Player level amount.
EXPERIENCE_AMOUNT = [40, 60, 100, 150, 210, 280, 700, 800, 900, 100000]

# Rounds stats.
ROUNDS_SPAWNS = [20, 40, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60]

# Chests
REWARD_POOL = ["orb", "wand", "aura", "fireball", "meteor", "addprojectile"]

# Orb stats.
ORB_REVOLUTION_RADIUS = 80
ORB_RADIUS = 30
