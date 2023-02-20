"""
Pig class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class Pig(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the pig.

            Args:
                parent (Game): The parent object that contain the pig
        """
        super().__init__(parent)
        self.type = "pig"
        self.frameAmount = 11