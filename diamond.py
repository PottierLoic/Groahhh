"""
Diamond class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random

class Diamond:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tag="diamond"
        self.value = random.randint(1, 10)