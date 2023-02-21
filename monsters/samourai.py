"""
Samourai class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class Samourai(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the samourai.

            Args:
                parent (Game): The parent object that contain the samourai
        """
        super().__init__(parent)
        self.type = "samourai"
        self.frameAmount = 11