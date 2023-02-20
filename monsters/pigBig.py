"""
PigBig class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class PigBig(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the pigBig.

            Args:
                parent (Game): The parent object that contain the pigBig
        """
        super().__init__(parent)
        self.type = "pigBig"
        self.frameAmount = 10
        self.boss = True