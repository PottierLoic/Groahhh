"""
Player class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import random
import math

# Local libraries.
from constants import *
from bullet import Bullet
from orb import Orb 

class Player:

    def __init__(self, parent, x, y) -> None:
        """
        Initialize the player.

            Args:
                parent (Game): The parent class of the player
                x (int): The x position of the player.
                y (int): The y position of the player.
        """
        # Global.
        self.parent = parent
        self.tag = "player"

        # Position.
        self.x = x
        self.y = y
        self.direction = (1, 1)
        
        # Movement.
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        # Health.
        self.maxHealth = 200
        self.health = 200

        # Level.
        self.level = 1
        self.exp = 0
    
        # Animation.
        self.animation = 0
        self.animationDelay = 0
        self.moving = False

        # Weapons.
        self.bullets = []
        self.orbs = []
        self.meteors = []

        self.fireDelay = 0
        self.addedProjectiles = 1
        
        self.haveWand = True
        self.wandLevel = 1

        self.haveOrb = True
        self.orbSpeed = 0.006
        self.orbAngle = 0
        self.orbLevel = 4

        self.haveMeteor = False
        self.meteorLevel = 0

        self.haveAura = False
        self.auraLevel = 0

        self.haveLaser = False
        self.laserLevel = 0

    def update(self):
        """Update the player position and status."""
        # Animation frame change
        if self.animationDelay < ANIMATION_SPEED:
            self.animationDelay += 1
        else:
            self.animation = (self.animation + 1) % 4
            self.animationDelay = 0

        # Weapons section
        if self.haveWand: self.wand()
        if self.haveAura: self.aura()
        if self.haveOrb: self.orb()
        if self.haveLaser: self.laser()
        if self.haveMeteor: self.meteor()
        
        for bullet in self.bullets:
            bullet.move()
        
        # Movement
        if self.left: self.x -= 1
        if self.right: self.x += 1
        if self.up: self.y -= 1
        if self.down: self.y += 1

        # Level up check
        if self.exp >= EXPERIENCE_AMOUNT[self.level-1]:
            self.level += 1
            self.exp = 0
            self.parent.rewardQueue.append([random.choice(self.parent.rewardPool) for _ in range(3)])
            self.parent.state = "reward"
        
    def wand(self):
        """Shoot a bullet."""
        if self.fireDelay <= 0:
            self.bullets.append(Bullet(self, self.direction))
            self.fireDelay = WEAPON_DELAY
        else:
            self.fireDelay -= self.wandLevel

    def aura(self):
        pass

    def meteor(self):
        pass

    def laser(self):
        pass

    def orb(self):
        """Calculate all orb positions"""
        self.orbs = []
        for i in range(self.orbLevel):
            theta = self.orbAngle+(6.28/self.orbLevel)*i
            x = self.x + ORB_REVOLUTION_RADIUS * math.cos(theta)
            y = self.y + ORB_REVOLUTION_RADIUS * math.sin(theta)
            self.orbs.append(Orb(x, y))
        self.orbAngle+=self.orbSpeed

    def upgrade(self, reward):
        """
        Upgrade the level of a weapon
        
            Args:
                reward (str): the weapon to be upgraded
        """
        print("Reward : ", reward)
        match reward:
            case "wand":
                self.wandLevel += 1
                if not self.haveWand : self.haveWand = True
            case "orb":
                if self.orbLevel < 7:
                    self.orbLevel += 1
                    self.orbSpeed += 0.001
                elif self.orbLevel < 8:
                    self.parent.rewardPool.remove("orb")
                    self.orbLevel = 8
                    self.orbSpeed = 0.02
                if not self.haveOrb : self.haveOrb = True
            case "meteor":
                self.meteorLevel += 1
                if not self.haveMeteor : self.haveMeteor = True
            case "laser":
                self.laserLevel += 1
                if not self.haveLaser : self.haveLaser = True
            case "aura":
                self.auraLevel += 1
                if not self.haveAura : self.haveAura = True
            