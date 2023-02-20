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
from fireball import Fireball

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
        self.speed = 0.5

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
        self.fireballs = []

        self.fireDelay = 0
        self.addedProjectiles = 0
        
        self.haveWand = True
        self.wandLevel = 1

        self.haveOrb = False
        self.orbSpeed = 0.006
        self.orbAngle = 0
        self.orbLevel = 0

        self.haveMeteor = False
        self.meteorLevel = 0

        self.haveAura = False
        self.auraLevel = 0

        self.haveFireball = False
        self.fireballLevel = 1
        self.fireballDelay = 0

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
        if self.haveFireball: self.fireball()
        if self.haveMeteor: self.meteor()
        
        for bullet in self.bullets:
            bullet.move()
        for fireball in self.fireballs:
            fireball.update()
        
        # Movement
        if self.left: self.x -= 1 * self.speed
        if self.right: self.x += 1 * self.speed
        if self.up: self.y -= 1 * self.speed
        if self.down: self.y += 1 * self.speed

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

    def fireball(self):
        """Shoot a fireball."""
        if self.fireballDelay <= 0:
            for i in range(self.fireballLevel):
                randomDirection = (math.cos(random.randint(0, 20)), math.sin(random.randint(0, 20)))
                self.fireballs.append(Fireball(self, randomDirection))
            self.fireballDelay = FIREBALL_DELAY
        else:
            self.fireballDelay -= self.fireballLevel

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
            case "fireball":
                self.fireballLevel += 1
                if not self.haveFireball : self.haveFireball = True
            case "aura":
                self.auraLevel += 1
                if not self.haveAura : self.haveAura = True
            