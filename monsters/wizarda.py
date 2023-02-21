"""
WizardA class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class WizardA(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the wizardA.

            Args:
                parent (Game): The parent object that contain the wizardA
        """
        super().__init__(parent)
        self.type = "wizarda"
        self.frameAmount = 11