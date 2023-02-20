"""
Orb class.
    Author : Loïc Pottier
    Creation date : 20/02/2023
"""

class Orb:
    def __init__(self, x, y) -> None:
        """
        Initialize the orb

            Args:
                x (int): The x position of the player.
                y (int): The y position of the player.
        """
        self.x = x
        self.y = y
        self.tag = "orb"