"""
Player class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.

# Local libraries.
from constants import *
from bullet import Bullet

class Player:

    def __init__(self, x = 0, y = 0) -> None:
        self.health = 100
        self.x = x
        self.y = y
        self.direction = (0, 0)
    
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.fire = False

        self.bullets = []
        self.weaponDelay = 0

    def update(self):
        if self.fire:
            self.shoot()
        for bullet in self.bullets:
            bullet.move()
        if self.left:
            self.x -= 1
        if self.right:
            self.x += 1
        if self.up:
            self.y -= 1
        if self.down:
            self.y += 1
        
    def shoot(self):
        if self.weaponDelay <= 0:
            self.bullets.append(Bullet(self, self.direction))
            self.weaponDelay = WEAPON_DELAY
        else:
            self.weaponDelay -= 1