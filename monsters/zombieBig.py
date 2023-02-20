"""
ZombieBig class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class ZombieBig(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the zombieBig.

            Args:
                parent (Game): The parent object that contain the zombieBig
        """
        super().__init__(parent)
        self.type = "zombieBig"
        self.frameAmount = 10
        self.boss = True