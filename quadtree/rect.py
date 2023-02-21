"""
Rect class
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

class Rect:
    def __init__(self, x, y, w, h) -> None:
        """
        Initialize the Rect.
        
            Args:
                x, y (int): coordinates of the rectangle
                w, h (int): dimensions of the rectangle(from the center)
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        """
        Check if the point is inside the rectangle.
        
            Args:
                point (Object): the point we want to find

            Returns:
                True if the point is contained in it, else returns False
        """
        return (point.x >= self.x - self.w and
                point.x <= self.x + self.w and
                point.y >= self.y - self.h and
                point.y <= self.y + self.h)

    def intersects(self, range):
        """
        Check if the rectangle intersects the range.
        
            Args:
                range (Rect): range to check
            
            Returns:
                True if the rectangle intersect the range, else returns False
        """
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)
    
    def draw(self, canvas, xoffset=0, yoffset=0):
        """
        Draw the rectangle.

            Args:
                canvas (Canvas): canvas where we want the rectangles to be drawed.
                xoffset, yoffset (int): offset needed for the canvas to display in the center of the screen.
        """
        canvas.create_rectangle(self.x-self.w - xoffset, self.y-self.h - yoffset, self.x+self.w - xoffset, self.y+self.h - yoffset, outline="red")
