"""
SkeletonBig class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class SkeletonBig(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the skeletonBig.

            Args:
                parent (Game): The parent object that contain the skeletonBig
        """
        super().__init__(parent)
        self.type = "skeletonBig"
        self.frameAmount = 11
        self.boss = True

