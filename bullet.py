"""
Bullet class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.

# Local libraries.
from constants import *


class Bullet:
    def __init__(self, parent, direction) -> None:
        """
        Initialize the bullet.

            Args:
                parent (Player): The player who shot the bullet.
                direction (tuple): The direction of the bullet.
        """
        self.parent = parent
        self.x = self.parent.x
        self.y = self.parent.y
        self.life = FALL_DISTANCE
        self.direction = direction


    def move(self):
        """Move the bullet."""
        self.x += self.direction[0] * BULLET_SPEED
        self.y += self.direction[1] * BULLET_SPEED
        self.life -= 1
        if self.life <= 0:
            self.parent.bullets.remove(self)
        if 0>self.x>WIDTH or 0>self.y>HEIGHT:
            self.parent.bullets.remove(self)