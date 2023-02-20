"""
Rect class
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

class Rect:
    def __init__(self, x, y, w, h) -> None:
        """Initialize the Rect."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point):
        """Check if the point is inside the rectangle."""
        return (point.x >= self.x - self.w and
                point.x <= self.x + self.w and
                point.y >= self.y - self.h and
                point.y <= self.y + self.h)

    def intersects(self, range):
        """Check if the rectangle intersects the range."""
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)
    
    def draw(self, canvas):
        """Draw the rectangle."""
        canvas.create_rectangle(self.x-self.w, self.y-self.h, self.x+self.w, self.y+self.h, outline="red")
