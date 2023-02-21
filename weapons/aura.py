"""
Aura class
    Author : Pottier Loïc
    Creation date : 21/02/2023
"""

# Basic libraries


# Local libraries
from constants import *

class Aura:
    def __init__(self, x, y, speed) -> None:
        """
        Initialize the aura.

            Args:
                x, y (int): Player position, aura and player have the same.
                speed (int): Damage are applied to enemies at this speed.
        """
        self.x = x
        self.y = y
        self.radius = 100
        self.animation = 0
        self.animationDelay = 0
        self.damageDelay = 0
        self.damageSpeed = speed

    def update(self, x, y, speed):
        """
        Update the aura.
        
            Args:
                x, y (int): new player position.
                speed: new aura speed.
        """
        self.speed = speed
        if self.animationDelay < AURA_ANIMATION_SPEED:
            self.animationDelay += 1
        else:
            self.animation = (self.animation + 1) % 29
            self.animationDelay = 0
        
        if self.damageDelay < self.speed:
            self.damageDelay += 1
        else:
            self.damageDelay = 0
        
        self.x = x
        self.y = y