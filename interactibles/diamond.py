"""
Diamond class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random

# Local libraries
from constants import *

class Diamond:
    def __init__(self, x, y):
        """
        Initialize the diamond
            
            Args:
                x (int): the x coordinate of the zombie that instantiate this
                y (int): the y coordinate of the zombie that instantiate this
        """
        # Global.
        self.tag="diamond"

        # Position.
        self.x = x
        self.y = y

        # Experience value
        self.value = random.randint(1, 10)

    def magnet(self, player):
        """
        Move the diamond in the player direction, only called when a magnet is active
        
             Args:
                parent (Game): The parent object that contain the diamond
        """
        distx = abs(player.x - self.x)
        disty = abs(player.y - self.y)
        if self.x < player.x:
            self.x += 0.1 * distx/(distx+disty) * MAGNET_SPEED
        elif self.x > player.x:
            self.x -= 0.1 * distx/(distx+disty) * MAGNET_SPEED
        if self.y < player.y:
            self.y += 0.1 * disty/(distx+disty) * MAGNET_SPEED
        elif self.y > player.y:
            self.y -= 0.1 * disty/(distx+disty) * MAGNET_SPEED