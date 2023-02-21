"""
QuadTree class
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Local libraries
from quadtree.node import Node

class QuadTree:
    def __init__(self, boundary, capacity) -> None:
        """
        Initialize the QuadTree.
        
            Args:
                boundary (Rect): Rectangle that represents the area we want to cover with the tree
                capacity (int): maximum number of objects a node can contain without subdividing
        """
        self.boundary = boundary
        self.capacity = capacity
        self.root = Node(boundary, capacity)

    def insert(self, point):
        """
        Insert a point in the QuadTree.
        
            Args:
                point (Object): the object we want to insert in the tree.
        """
        self.root.insert(point)

    def query(self, range, found):
        """
        Query the quadtree.
        
            Args:
                range (Rect): rectangle object that represents the zone we want to check
                found (list): list that will be filled with all the objects found
        """
        self.root.query(range, found)

    def draw(self, canvas, xoffset=0, yoffset=0):
        """
        Draw the quadtree.
        
            Args:
                canvas (Canvas): canvas where we want the rectangles to be drawed.
                xoffset, yoffset (int): offset needed for the canvas to display in the center of the screen.
        """
        self.root.draw(canvas, xoffset, yoffset)