"""
Magnet class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random

class Magnet:
    def __init__(self, x, y):
        """
        Initialize the magnet
            
            Args:
                x (int): the x coordinate of the zombie that instantiate this
                y (int): the y coordinate of the zombie that instantiate this
        """
        # Global.
        self.tag="magnet"

        # Position.
        self.x = x
        self.y = y

