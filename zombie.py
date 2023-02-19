"""
Zombie class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random

# Local libraries.
from constants import *

class Zombie:
    def __init__(self, parent) -> None:
        """
        Initialize the zombie.

            Args:
                parent (Game): The game where the zombie is.
        """
        self.parent = parent
        self.health = 40

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
        
        self.hit_delay = 0
        self.animationDelay = 0
        self.animation = 0
    
    def update(self, player):
        """
        Update the zombie position status and animation state.

            Args:
                player (Player): The player.
        """
        if self.animationDelay < ANIMATION_SPEED:
            self.animationDelay += 1
        else:
            self.animation = (self.animation + 1) % 5
            self.animationDelay = 0

        if self.health <= 0:
            self.parent.zombies.remove(self)

        distx = abs(player.x - self.x)
        disty = abs(player.y - self.y)

        if self.x < player.x:
            self.x += 0.1 * distx/(distx+disty) * ZOMBIE_SPEED
        if self.x > player.x:
            self.x -= 0.1 * distx/(distx+disty) * ZOMBIE_SPEED
        if self.y < player.y:
            self.y += 0.1 * disty/(distx+disty) * ZOMBIE_SPEED
        if self.y > player.y:
            self.y -= 0.1 * disty/(distx+disty) * ZOMBIE_SPEED

