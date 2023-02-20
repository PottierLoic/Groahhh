"""
Zombie class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random

# Local libraries.
from constants import *
from diamond import Diamond
from chest import Chest

class Zombie:
    def __init__(self, parent) -> None:
        """
        Initialize the zombie.

            Args:
                parent (Game): The parent object that contain the zombie
        """
        # Global.
        self.parent = parent
        self.tag = "zombie"
        
        # Health
        self.maxHealth = 20
        self.health = 20

        # Attack.
        self.hit_delay = 0
        
        # Animation.
        self.animationDelay = 0
        self.animation = 0

        # Position outside of the safe zone.
        if random.randrange(2) == 0:
            x1 = random.randint(self.parent.player.x - SPAWN_RANGE, self.parent.player.x - SAFE_DISTANCE)
            x2 = random.randint(self.parent.player.x + SAFE_DISTANCE, self.parent.player.x + SPAWN_RANGE)
            self.x = random.choice([x1, x2])
            self.y = random.randint(self.parent.player.y - SPAWN_RANGE, self.parent.player.y + SPAWN_RANGE)
        else:
            y1 = random.randint(self.parent.player.y - SPAWN_RANGE, self.parent.player.y - SAFE_DISTANCE)
            y2 = random.randint(self.parent.player.y + SAFE_DISTANCE, self.parent.player.y + SPAWN_RANGE)
            self.y = random.choice([y1, y2])
            self.x = random.randint(self.parent.player.x - SPAWN_RANGE, self.parent.player.x + SPAWN_RANGE)
    
    def update(self, player):
        """
        Update the zombie position status and animation state.

            Args:
                player (Player): The player.
        """
        # Animation frame change
        if self.animationDelay < ANIMATION_SPEED:
            self.animationDelay += 1
        else:
            self.animation = (self.animation + 1) % 5
            self.animationDelay = 0

        # Death check and diamond random spawn
        if self.health <= 0:
            if random.randrange(100) > DIAMOND_SPAWN_CHANCE:
                self.parent.diamonds.append(Diamond(self.x, self.y))
            if random.randrange(100) > CHEST_SPAWN_CHANCE:
                self.parent.chests.append(Chest(self.parent, self.x, self.y))
            self.parent.zombies.remove(self)

        # Move in the player direction
        distx = abs(player.x - self.x)
        disty = abs(player.y - self.y)
        if self.x < player.x:
            self.x += 0.1 * distx/(distx+disty) * ZOMBIE_SPEED
        elif self.x > player.x:
            self.x -= 0.1 * distx/(distx+disty) * ZOMBIE_SPEED
        if self.y < player.y:
            self.y += 0.1 * disty/(distx+disty) * ZOMBIE_SPEED
        elif self.y > player.y:
            self.y -= 0.1 * disty/(distx+disty) * ZOMBIE_SPEED

