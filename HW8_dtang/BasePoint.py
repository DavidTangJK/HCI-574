# BasePoint class definition
import turtle

class BasePoint:
    ''' A rudimentary point class '''

    def __init__(self, x_coord=0, y_coord=0):
        "Create instance from a x and a y coordinate"
        self.x = x_coord
        self.y = y_coord
        #print(id(self), self.__class__.__name__,  self.x, self.y)

    def get_xy(self):
        return (self.x, self.y) # return x/y pair in a tuple
    
    def set_x(self, new_x):
        self.x = new_x

    def __str__(self):
        "return string with x and y coordinates ( for print() )"
        return  "x: " + str(self.x) + ", y: " + str(self.y)

    def __add__(self, other_point):
        "overloaded addition (+) operator"
        added_x = self.x + other_point.x
        added_y = self.y + other_point.y
        added_pt = BasePoint(added_x, added_y)
        return added_pt # return new, "added" up instance


    def draw(self, pen_size=3):
        "Go to x/y location and make a dot of size pen_size"
        turtle.penup()
        turtle.goto(self.x, self.y)
        old_pen_size = turtle.pensize() # store pensize
        turtle.pensize(pen_size)
        turtle.pendown()
        turtle.dot() # makes a dot
        turtle.pensize(old_pen_size) # restore old pen size
        turtle.penup()
