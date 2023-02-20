"""
Game class.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
import math

# Local libraries.
from constants import *
from player import Player
from zombie import Zombie
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
        self.spawnLeft = ROUNDS_SPAWNS[self.round-1]
        self.spawnDelay = SPAWN_DELAY
        self.rewardQueue = []
        self.rewardPool = REWARD_POOL

        # quadtree (used for optimization).
        self.quadtree = QuadTree(Rect(0, 0, WIDTH, HEIGHT), 4)

    def start(self):
        """Start the game."""
        self.state = "running"
        self.zombies = [Zombie(self) for _ in range(10)]
        self.round = 1

    def reset(self):
        """Reset the game."""
        self.__init__()

    def update(self):
        """Update the game."""
        if self.state == "running":

            self.player.exp+=0.2
            # Position updates
            self.player.update()
            for zombie in self.zombies:
                zombie.update(self.player)
            for chest in self.chests:
                chest.update()


            """NEED TO WORK ON THOSES
            MUST NOT RECREATE QUADTREE 3-4 TIME, 
            MUST FILL IT WITH VERYTHING AND CHECK ONE TIME EACH OBJECT"""
            # Player quadtree collision check
            nearby = []
            self.quadtree = QuadTree(Rect(0, 0, WIDTH, HEIGHT), 4)
            self.quadtree.insert(self.player)
            for zombie in self.zombies:
                self.quadtree.insert(zombie)
            for diamond in self.diamonds:
                self.quadtree.insert(diamond)
            for chest in self.chests:
                self.quadtree.insert(chest)
            self.quadtree.query(Rect(self.player.x, self.player.y, PLAYER_HITBOX, PLAYER_HITBOX), nearby)

            for obj in nearby:
                if obj != self.player:
                    if obj.tag == "zombie":
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

            # Projectiles quadtree collision check
            nearby = []
            self.quadtree = QuadTree(Rect(0, 0, WIDTH, HEIGHT), 4)
            for zombie in self.zombies:
                self.quadtree.insert(zombie)
            for bullet in self.player.bullets:
                self.quadtree.insert(bullet)
                self.quadtree.query(Rect(bullet.x, bullet.y, 10, 10), nearby)
                for zombie in nearby:
                    if zombie.tag == "zombie":
                        if math.sqrt((bullet.x - zombie.x)**2 + (bullet.y - zombie.y)**2) < BULLET_SIZE/2 + ZOMBIE_SIZE/2:
                            zombie.health -= 10
                            try:
                                self.player.bullets.remove(bullet)
                            except:
                                pass

            nearby = []
            self.quadtree = QuadTree(Rect(0, 0, WIDTH, HEIGHT), 4)
            for zombie in self.zombies:
                self.quadtree.insert(zombie)
            for orb in self.player.orbs:
                self.quadtree.insert(orb)
                self.quadtree.query(Rect(orb.x, orb.y, ORB_RADIUS, ORB_RADIUS), nearby)
                for obj in nearby:
                    if obj.tag == "zombie":
                        if math.sqrt((orb.x - obj.x)**2 + (orb.y - obj.y)**2) < ORB_RADIUS/2 + ZOMBIE_SIZE/2:
                            obj.health -= 100

            # Spawn zombies
            if self.spawnLeft <= 0:
                self.round += 1
                self.spawnLeft = ROUNDS_SPAWNS[self.round-1]
            else:
                if self.spawnDelay <= 0:
                    self.zombies.append(Zombie(self))
                    self.spawnLeft -= 1
                    self.spawnDelay = SPAWN_DELAY
                else:
                    self.spawnDelay -= 1
                
            # Game over check
            if self.player.health <= 0:
                self.reset()

    def chooseReward(self, reward):
        self.player.upgrade(self.rewardQueue[0][reward])
        self.rewardQueue.pop(0)
        if len(self.rewardQueue) == 0:
            self.state = "running"