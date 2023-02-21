"""
WizardC class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries.
from constants import *
from monsters.monster import Monster

class WizardC(Monster):
    def __init__(self, parent) -> None:
        """
        Initialize the wizardC.

            Args:
                parent (Game): The parent object that contain the wizardC
        """
        super().__init__(parent)
        self.type = "wizardc"
        self.frameAmount = 11