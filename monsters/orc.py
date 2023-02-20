"""
Orc class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class Orc(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the orc.

            Args:
                parent (Game): The parent object that contain the orc
        """
        super().__init__(parent)
        self.type = "orc"
        self.frameAmount = 11