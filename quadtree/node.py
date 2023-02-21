"""
Node class
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries
from quadtree.rect import Rect

class Node:
    def __init__(self, boundary, capacity) -> None:
        """
        Initialize the Node.
        
            Args:
                boundary (Rect): Rectangle that represents the area we want to cover with the tree
                capacity (int): maximum number of objects a node can contain without subdividing
        """
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
        """
        Insert a point in the node.
        
            Args:
                point (Object): the object we want to insert in the node.
            
            Returns:
                False if it can't contain the point, else returns True and add the point to a node
        """
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
        """
        Query the node.
        
            Args:
                range (Rect): rectangle object that represents the zone we want to check
                found (list): list that will be filled with all the objects found
        """
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
        """
        Draw the node.
        
            Args:
                canvas (Canvas): canvas where we want the rectangles to be drawed.
                xoffset, yoffset (int): offset needed for the canvas to display in the center of the screen.
        """
        self.boundary.draw(canvas, xoffset, yoffset)
        if self.divided:
            self.northeast.draw(canvas, xoffset, yoffset)
            self.northwest.draw(canvas, xoffset, yoffset)
            self.southeast.draw(canvas, xoffset, yoffset)
            self.southwest.draw(canvas, xoffset, yoffset)