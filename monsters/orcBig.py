"""
OrcBig class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class OrcBig(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the orcBig.

            Args:
                parent (Game): The parent object that contain the orcBig
        """
        super().__init__(parent)
        self.type = "orcBig"
        self.frameAmount = 11
        self.boss = True