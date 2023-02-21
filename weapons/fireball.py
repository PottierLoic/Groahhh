"""
Fireball class.
    Author : Loïc Pottier
    Creation date : 20/02/2023
"""

# Basic libraries.
import math

# Local libraries.
from constants import *

class Fireball:
    def __init__(self, parent, direction) -> None:
        """
        Initialize the bullet.

            Args:
                parent (Player): The player who shot the fireball.
                direction (tuple): The direction of the fireball.
        """
        self.tag = "fireball"
        self.parent = parent
        self.x = self.parent.x
        self.y = self.parent.y
        self.health = FALL_DISTANCE_FIREBALL
        self.direction = direction
        
        # Animation.
        self.animation = 0
        self.animationDelay = 0
    
    def update(self):
        """Update fireball animationFrame"""
        # Animation frame change
        self.move()
        if self.animationDelay < ANIMATION_SPEED:
            self.animationDelay += 1
        else:
            self.animation = (self.animation + 1) % 4
            self.animationDelay = 0

    def move(self):
        """Move the fireball."""
        self.x += self.direction[0] * FIREBALL_SPEED
        self.y += self.direction[1] * FIREBALL_SPEED
        self.health -= 1
        if self.health <= 0:
            self.parent.fireballs.remove(self)
