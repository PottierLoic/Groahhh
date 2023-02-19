"""
Zombie class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random

# Local libraries.
from constants import *

class Zombie:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.health = 40
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
    
    def update(self, player):
        if self.health <= 0:
            self.parent.zombies.remove(self)

        if self.x < player.x:
            self.x += 0.1 * ZOMBIE_SPEED
        if self.x > player.x:
            self.x -= 0.1 * ZOMBIE_SPEED
        if self.y < player.y:
            self.y += 0.1 * ZOMBIE_SPEED
        if self.y > player.y:
            self.y -= 0.1 * ZOMBIE_SPEED

