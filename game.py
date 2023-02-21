"""
Game class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import math
import random

# Local libraries.
from constants import *
from player import Player
from monsters.zombie import Zombie
from monsters.zombieBig import ZombieBig
from monsters.skeleton import Skeleton
from monsters.skeletonBig import SkeletonBig
from monsters.orc import Orc
from monsters.orcBig import OrcBig
from monsters.pig import Pig
from monsters.pigBig import PigBig
from monsters.knight import Knight
from monsters.samourai import Samourai
from monsters.wizarda import WizardA
from monsters.wizardb import WizardB
from monsters.wizardc import WizardC

from quadtree.qtree import QuadTree
from quadtree.rect import Rect


class Game():
    def __init__(self) -> None:
        """Initialize the game."""

        # Objects.
        self.player = Player(self, WIDTH/2, HEIGHT/2)
        self.zombies = []
        self.diamonds = []
        self.chests = []

        # Game states
        self.state = "menu"
        self.round = 1
        self.roundDelay = ROUND_DELAY
        self.bossSpawned = False
        self.spawnLeft = ROUNDS_SPAWNS[self.round-1]
        self.spawnDelay = SPAWN_DELAY
        self.rewardQueue = []
        self.rewardPool = REWARD_POOL

        # quadtree (used for optimization).
        self.quadtree = QuadTree(Rect(0, 0, WIDTH, HEIGHT), CAPACITY)

    def start(self):
        """Start the game."""
        self.state = "running"
        self.monsters = []
        self.round = 5

    def reset(self):
        """Reset the game."""
        self.__init__()

    def update(self):
        """Update the game."""
        if self.state == "running":
            # Position and animation updates
            self.player.exp += 1
            self.player.update()
            for monster in self.monsters:
                monster.update(self.player)
            for chest in self.chests:
                chest.update()
            

            # Filling the quadtree
            self.quadtree = QuadTree(Rect(self.player.x, self.player.y, WIDTH, HEIGHT), CAPACITY)
            for monster in self.monsters:
                self.quadtree.insert(monster)
            for diamond in self.diamonds:
                self.quadtree.insert(diamond)
            for chest in self.chests:
                self.quadtree.insert(chest)
            
            # Player collision
            monsterToAim = []
            nearby = []
            self.quadtree.query(Rect(self.player.x, self.player.y, PLAYER_HITBOX, PLAYER_HITBOX), nearby)
            for obj in nearby:
                if obj.tag == "monster":
                    if math.sqrt((self.player.x - obj.x)**2 + (self.player.y - obj.y)**2) < PLAYER_HITBOX + ZOMBIE_SIZE/2:
                        if obj.hit_delay <= 0:
                            obj.hit_delay = HIT_DELAY
                            self.player.health -= 10
                        else:
                            obj.hit_delay -= 1
                elif obj.tag == "diamond":
                    if math.sqrt((self.player.x - obj.x)**2 + (self.player.y - obj.y)**2) < PLAYER_HITBOX + DIAMOND_SIZE/2:
                        self.player.exp += obj.value
                        self.diamonds.remove(obj)
                elif obj.tag == "chest":
                        if obj.oppened == False:
                            if math.sqrt((self.player.x - obj.x)**2 + (self.player.y - obj.y)**2) < PLAYER_HITBOX + CHEST_SIZE/2:
                                self.rewardQueue.append([obj.reward, None])
                                self.chooseReward(0)
                                obj.open()

            # Updating player direction to the nearest monster
            self.quadtree.query(Rect(self.player.x, self.player.y, 150, 150), nearby)
            for obj in nearby:
                if obj.tag == "monster":
                    monsterToAim.append(obj)
            if len(monsterToAim) > 0:
                min = 100000
                minx, miny = 0, 0
                for monster in monsterToAim:
                    if math.sqrt((self.player.x - monster.x)**2 + (self.player.y - monster.y)**2) < min:
                        min = math.sqrt((self.player.x - monster.x)**2 + (self.player.y - monster.y)**2)
                        minx, miny = monster.x, monster.y
                angle = math.atan2(miny - self.player.y, minx - self.player.x)
                self.player.direction = (math.cos(angle), math.sin(angle))
            else:
                self.player.direction = (math.cos(random.uniform(0, 2*math.pi)), math.sin(random.uniform(0, 2*math.pi)))

            # Bullet collision check.
            for bullet in self.player.bullets:
                self.quadtree.query(Rect(bullet.x, bullet.y, 5, 5), nearby)
                for obj in nearby:
                    if obj.tag == "monster":
                        if math.sqrt((bullet.x - obj.x)**2 + (bullet.y - obj.y)**2) < ZOMBIE_SIZE/2:
                            obj.health -= 10
                            try:
                                self.player.bullets.remove(bullet)
                            except:
                                pass   

            # Orb collision check        
            for orb in self.player.orbs:
                self.quadtree.query(Rect(orb.x, orb.y, ORB_RADIUS, ORB_RADIUS), nearby)
                for obj in nearby:
                    if obj.tag == "monster":
                        if math.sqrt((orb.x - obj.x)**2 + (orb.y - obj.y)**2) < ORB_RADIUS/2 + ZOMBIE_SIZE/2:
                            obj.health -= 100

            # Fireball collision check
            for fireball in self.player.fireballs:
                self.quadtree.query(Rect(fireball.x, fireball.y, FIREBALL_SIZE, FIREBALL_SIZE), nearby)
                for obj in nearby:
                    if obj.tag == "monster":
                        if math.sqrt((fireball.x - obj.x)**2 + (fireball.y - obj.y)**2) < FIREBALL_SIZE/2 + ZOMBIE_SIZE/2:
                            obj.health -= 50
                            fireball.health -= 50

            # Aura collision check
            if self.player.auras:
                if self.player.auras.damageDelay == 0:
                    self.quadtree.query(Rect(self.player.x, self.player.y, self.player.auraRadius, self.player.auraRadius), nearby)
                    for obj in nearby:
                        if obj.tag == "monster":
                            if math.sqrt((self.player.x - obj.x)**2 + (self.player.y - obj.y)**2) < self.player.auraRadius/2 + ZOMBIE_SIZE/2:
                                obj.health -= 5

            # Meteor collision check
            for meteor in self.player.meteors:
                if meteor.explodeDelay == 0:
                    self.quadtree.query(Rect(meteor.x, meteor.y, METEOR_SIZE/2, METEOR_SIZE/2), nearby)
                    for obj in nearby:
                        if obj.tag == "monster":
                            if math.sqrt((meteor.x - obj.x)**2 + (meteor.y - obj.y)**2) < METEOR_SIZE/2 + ZOMBIE_SIZE/2:
                                obj.health -= 100

            # Monster spawn
            if self.spawnLeft <= 0 and self.bossSpawned == False:
                self.spawnBoss()
            else:
                self.spawn()

            if self.bossSpawned:
                self.roundDelay -= 1

            if self.roundDelay <= 0:
                if self.round < 10:
                    self.round += 1
                self.bossSpawned = False
                self.spawnLeft = ROUNDS_SPAWNS[self.round-1]
                self.roundDelay = ROUND_DELAY
                
            # Game over check
            if self.player.health <= 0:
                self.reset()

    def spawn(self):
        """Spawn monster."""
        if self.spawnDelay <= 0:
            match self.round:
                case 1:
                    self.monsters.append(Zombie(self))
                case 2:
                    self.monsters.append(Skeleton(self))
                case 3:
                    self.monsters.append(Orc(self))
                case 4:
                    self.monsters.append(Pig(self))
                case 5:
                    self.monsters.append(Knight(self))
                case 6:
                    self.monsters.append(WizardA(self))
                case 7:
                    self.monsters.append(WizardB(self))
                case 8:
                    self.monsters.append(WizardC(self))
                case 9:
                    self.monsters.append(Samourai(self))
                case _:
                    self.monsters.append(random.choice([Zombie(self), Skeleton(self), Orc(self), Pig(self), Knight(self), WizardA(self), WizardB(self), WizardC(self), Samourai(self)]))
            if self.spawnLeft != 0:
                self.spawnLeft -= 1
            self.spawnDelay = SPAWN_DELAY
        else:
            self.spawnDelay -= 1

    def spawnBoss(self):
        """Spawn boss."""
        self.bossSpawned = True
        match self.round:
            case 1:
                self.monsters.append(ZombieBig(self))
            case 2:
                self.monsters.append(SkeletonBig(self))
            case 3:
                self.monsters.append(OrcBig(self))
            case 4:
                self.monsters.append(PigBig(self))
            case _:
                self.monsters.append(random.choice([ZombieBig(self), SkeletonBig(self), OrcBig(self), PigBig(self)]))
            

    def chooseReward(self, reward):
        """
        Upgrade the player with the choosen reward
        
            Args:
                reward (int): index of the choosenReward in rewardQueue
        """
        self.player.upgrade(self.rewardQueue[0][reward])
        self.rewardQueue.pop(0)
        if len(self.rewardQueue) == 0:
            self.state = "running"