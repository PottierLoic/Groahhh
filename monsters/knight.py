"""
Knight class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class Knight(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the knight.

            Args:
                parent (Game): The parent object that contain the knight
        """
        super().__init__(parent)
        self.type = "knight"
        self.frameAmount = 11