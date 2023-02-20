"""
QuadTree class
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries
from quadtree.node import Node

class QuadTree:
    def __init__(self, boundary, capacity) -> None:
        """Initialize the QuadTree."""
        self.boundary = boundary
        self.capacity = capacity
        self.root = Node(boundary, capacity)

    def insert(self, point):
        """Insert a point in the QuadTree."""
        self.root.insert(point)

    def query(self, range, found):
        """Query the QuadTree."""
        self.root.query(range, found)

    def draw(self, canvas):
        """Draw the QuadTree."""
        self.root.draw(canvas)