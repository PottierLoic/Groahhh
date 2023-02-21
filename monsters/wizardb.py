"""
WizardB class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class WizardB(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the wizardB.

            Args:
                parent (Game): The parent object that contain the wizardB
        """
        super().__init__(parent)
        self.type = "wizardb"
        self.frameAmount = 11