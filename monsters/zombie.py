"""
Zombie class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class Zombie(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the zombie.

            Args:
                parent (Game): The parent object that contain the zombie
        """
        super().__init__(parent)
        self.type = "zombie"
        self.frameAmount = 11