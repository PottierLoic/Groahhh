"""
Skeleton class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class Skeleton(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the skeleton.

            Args:
                parent (Game): The parent object that contain the skeleton
        """
        super().__init__(parent)
        self.type = "skeleton"
        self.frameAmount = 10

