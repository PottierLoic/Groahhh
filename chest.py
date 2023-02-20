"""
Chest class.
    Author : Loïc Pottier
    Creation date : 20/02/2023
"""

#Basic libraries.
import random

# Local libraries
from constants import *

class Chest:
    def __init__(self, parent, x, y) -> None:

        # Global.
        self.tag = "chest"
        self.parent = parent
        self.health = 100
        
        # Position.
        self.x = x
        self.y = y

        # Reward
        self.reward = random.choice(parent.rewardPool)

        # Animation.
        self.oppened = False
        self.animation = 0
        self.animationDelay = 0

    def update(self):
        """Update the animation frames once the chest is oppened"""
        if self.oppened:
            self.health-=1
            if self.animationDelay < ANIMATION_SPEED:
                self.animationDelay += 1
            else:
                if self.animation < 2:
                    self.animation += 1
                    self.animationDelay = 0

            if self.health < 0:
                self.parent.chests.remove(self)

    def open(self):
        self.oppened = True