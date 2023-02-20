"""
Node class
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries
from quadtree.rect import Rect

class Node:
    def __init__(self, boundary, capacity) -> None:
        """Initialize the Node."""
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        """Subdivide the node."""
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rect(x + w / 2, y - h / 2, w / 2, h / 2)
        nw = Rect(x - w / 2, y - h / 2, w / 2, h / 2)
        se = Rect(x + w / 2, y + h / 2, w / 2, h / 2)
        sw = Rect(x - w / 2, y + h / 2, w / 2, h / 2)

        self.northeast = Node(ne, self.capacity)
        self.northwest = Node(nw, self.capacity)
        self.southeast = Node(se, self.capacity)
        self.southwest = Node(sw, self.capacity)
        self.divided = True

    def insert(self, point):
        """Insert a point in the node."""
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(point):
                return True
            elif self.northwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True

    def query(self, range, found):
        """Query the node."""
        if not self.boundary.intersects(range):
            return

        for point in self.points:
            if range.contains(point):
                found.append(point)

        if self.divided:
            self.northeast.query(range, found)
            self.northwest.query(range, found)
            self.southeast.query(range, found)
            self.southwest.query(range, found)

    def draw(self, canvas, xoffset=0, yoffset=0):
        """Draw the node."""
        self.boundary.draw(canvas, xoffset, yoffset)
        if self.divided:
            self.northeast.draw(canvas, xoffset, yoffset)
            self.northwest.draw(canvas, xoffset, yoffset)
            self.southeast.draw(canvas, xoffset, yoffset)
            self.southwest.draw(canvas, xoffset, yoffset)