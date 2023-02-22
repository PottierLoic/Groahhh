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
from weapons.bullet import Bullet
from weapons.orb import Orb 
from weapons.fireball import Fireball
from weapons.aura import Aura
from weapons.meteor import Meteor

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
        self.speed = 1.5

        # Health.
        self.maxHealth = 200000
        self.health = 200000

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
        self.auras = None

        self.fireDelay = 0
        self.addedProjectiles = 0
        
        self.haveWand = True
        self.wandLevel = 1

        self.haveOrb = False
        self.orbSpeed = 0.006
        self.orbAngle = 0
        self.orbLevel = 0
        self.orbAnimation = 0
        self.orbAnimationDelay = 0

        self.haveMeteor = False
        self.meteorLevel = 0
        self.meteorDelay = 0

        self.haveAura = False
        self.auraLevel = 0
        self.auraRadius = 100

        self.haveFireball = False
        self.fireballLevel = 0
        self.fireballDelay = 0

    def update(self):
        """Update the player position and status."""
        # Animation frame change
        if self.animationDelay < ANIMATION_SPEED:
            self.animationDelay += 1
        else:
            self.animation = (self.animation + 1) % 4
            self.animationDelay = 0

        # Orb animation frame change
        if self.orbAnimationDelay < ORB_ANIMATION_SPEED:
            self.orbAnimationDelay += 1
        else:
            self.orbAnimation = (self.orbAnimation + 1) % 7
            self.orbAnimationDelay = 0
        
        # Movement
        if self.left: self.x -= 1 * self.speed
        if self.right: self.x += 1 * self.speed
        if self.up: self.y -= 1 * self.speed
        if self.down: self.y += 1 * self.speed

        # Weapons section
        if self.haveWand: self.wand()
        if self.haveAura: self.aura()
        if self.haveOrb: self.orb()
        if self.haveFireball: self.fireball()
        if self.haveMeteor: self.meteor()

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
        for bullet in self.bullets:
            bullet.move()

    def aura(self):
        """Modify the aura position and radius"""
        if self.auras == None: self.auras = Aura(self.x, self.y, 120 * (1/self.auraLevel))
        self.auraRadius = 100 * self.auraLevel
        self.auras.update(self.x, self.y, 120 * (1/self.auraLevel))

    def meteor(self):
        """Trigger meteor fall once the delay is done and update them"""
        if self.meteorDelay <= 0:
            for i in range(self.meteorLevel + self.addedProjectiles):
                randomx = random.uniform(self.x - WIDTH/2, self.x + WIDTH/2)
                randomy = random.uniform(self.y - HEIGHT/2, self.y + HEIGHT/2)
                self.meteors.append(Meteor(self, randomx, randomy))
                self.meteorDelay = METEOR_DELAY
        else:
            self.meteorDelay -= self.meteorLevel
        for meteor in self.meteors:
            meteor.update()

    def fireball(self):
        """Shoot a fireball."""
        if self.fireballDelay <= 0:
            for i in range(self.fireballLevel + self.addedProjectiles):
                randomDirection = (math.cos(random.uniform(0, 2*math.pi)), math.sin(random.uniform(0, 2*math.pi)))
                self.fireballs.append(Fireball(self, randomDirection))
            self.fireballDelay = FIREBALL_DELAY
        else:
            self.fireballDelay -= self.fireballLevel
        for fireball in self.fireballs:
            fireball.update()

    def orb(self):
        """Calculate all orb positions and update their animation state"""
        self.orbs = []
        for i in range(self.orbLevel + self.addedProjectiles):
            theta = self.orbAngle+(6.28/(self.orbLevel + self.addedProjectiles))*i
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
                    self.orbSpeed += 0.005
                elif self.orbLevel < 8:
                    self.parent.rewardPool.remove("orb")
                    self.orbLevel = 8
                    self.orbSpeed = 0.05
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
            case "addprojectile":
                self.addedProjectiles += 1
            