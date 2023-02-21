"""
Food class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random

class Food:
    def __init__(self, x, y):
        """
        Initialize the food
            
            Args:
                x (int): the x coordinate of the zombie that instantiate this
                y (int): the y coordinate of the zombie that instantiate this
        """
        # Global.
        self.tag="food"
        self.animation = random.randint(0, 3)

        # Position.
        self.x = x
        self.y = y

        # health value
        self.value = random.randint(20, 80)

