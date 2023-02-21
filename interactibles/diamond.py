"""
Diamond class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random

class Diamond:
    def __init__(self, x, y):
        """
        Initialize the diamon
            
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