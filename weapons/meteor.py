"""
Metor class.
    Author : Loïc Pottier
    Creation date : 21/02/223
"""

# Local libraries
from constants import *

class Meteor:
    def __init__(self, parent, x, y) -> None:
        """
        Initialize the meteor.

            Args:
                parent (Player): The player who shot the meteor.
                x, y (int): random coords where the meteor will fall.
        """
        self.parent = parent
        self.x = x
        self.y = y
        self.animation = 0
        self.animationDelay = 0
        self.explodeDelay = 60

    def update(self):
        """Update the meteor"""
        if self.animationDelay < METEOR_ANIMATION_SPEED:
            self.animationDelay += 1
        else:
            self.animation = (self.animation + 1) % 10
            self.animationDelay = 0

        self.explodeDelay -= 1

        if self.explodeDelay < 0:
            self.parent.meteors.remove(self)
