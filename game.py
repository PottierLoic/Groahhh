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
        self.player = Player(WIDTH/2, HEIGHT/2)
        self.zombies = []
        self.diamonds = []
        self.state = "menu"
        self.round = 1
        self.spawnLeft = ROUNDS_SPAWNS[self.round-1]
        self.spawnDelay = SPAWN_DELAY
        self.quadtree = QuadTree(Rect(0, 0, WIDTH, HEIGHT), 4)

    def start(self):
        """Start the game."""
        self.state = "running"
        self.zombies = [Zombie(self) for _ in range(10)]
        self.player = Player(WIDTH/2, HEIGHT/2)
        self.round = 1

    def reset(self):
        """Reset the game."""
        self.__init__()

    def update(self):
        """Update the game."""
        self.player.update()
        for zombie in self.zombies:
            zombie.update(self.player)

        # Quadtree collision

        # Player collision
        nearby = []
        self.quadtree = QuadTree(Rect(0, 0, WIDTH, HEIGHT), 4)
        self.quadtree.insert(self.player)
        for zombie in self.zombies:
            self.quadtree.insert(zombie)
        for diamond in self.diamonds:
            self.quadtree.insert(diamond)
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

        # Bullet collision
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
            
        if self.player.health <= 0:
            self.reset()

 