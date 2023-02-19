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

class Game():
    def __init__(self) -> None:
        """Initialize the game."""
        self.player = Player(WIDTH/2, HEIGHT/2)
        self.zombies = []
        self.state = "menu"
        self.round = 1
        self.spawnDelay = SPAWN_DELAY

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

        self.collision()
        if self.spawnDelay <= 0:
            self.zombies.append(Zombie(self))
            self.spawnDelay = SPAWN_DELAY
        else:
            self.spawnDelay -= 1

        if self.player.health <= 0:
            self.reset()

    def collision(self):
        """Check the collision between all objects."""
        for zombie in self.zombies:
            if math.sqrt((self.player.x - zombie.x)**2 + (self.player.y - zombie.y)**2) < PLAYER_SIZE + ZOMBIE_SIZE:
                if zombie.hit_delay <= 0:
                    zombie.hit_delay = HIT_DELAY
                    self.player.health -= 10
                else:
                    zombie.hit_delay -= 1
            for bullet in self.player.bullets:
                if math.sqrt((bullet.x - zombie.x)**2 + (bullet.y - zombie.y)**2) < BULLET_SIZE + ZOMBIE_SIZE:
                    zombie.health -= 10
                    self.player.bullets.remove(bullet)