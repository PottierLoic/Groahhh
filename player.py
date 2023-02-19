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
        """
        Initialize the player.

            Args:
                x (int): The x position of the player.
                y (int): The y position of the player.
        """
        self.x = x
        self.y = y
        self.direction = (0, 0)
        
        self.maxHealth = 200
        self.health = 200
    
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.fire = False
        self.animation = 0
        self.animationDelay = 0
        self.moving = False

        self.bullets = []
        self.fireDelay = 0

    def update(self):
        """Update the player position and status."""
        if self.animationDelay < ANIMATION_SPEED:
            self.animationDelay += 1
        else:
            self.animation = (self.animation + 1) % 4
            self.animationDelay = 0

        if self.fire: self.shoot()

        for bullet in self.bullets:
            bullet.move()
        
        if self.left: self.x -= 1
        if self.right: self.x += 1
        if self.up: self.y -= 1
        if self.down: self.y += 1
        
    def shoot(self):
        """
        Shoot a bullet.
        """
        if self.fireDelay <= 0:
            self.bullets.append(Bullet(self, self.direction))
            self.fireDelay = WEAPON_DELAY
        else:
            self.fireDelay -= 1