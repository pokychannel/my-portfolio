from textwrap import fill
from tkinter import * 
root = Tk()
canvas = Canvas(root, width=400, height=400)
root.title("Bezier curve")

canvas.pack()
d=7

class Bezier():

    def __init__(self):
        self.item = 0; self.previous = (0, 0); self.click_number = 0
        self.p1 = (0, 0); self.p2 = (0, 0); self.p3 = (0, 0); self.p4 = (0, 0)

    def draw_point(self, p, tag):
        canvas.create_rectangle(p[0]-2, p[1]-2, p[0]+2, p[1]+2, tags=tag)

    def draw_line(self, p1, p2, tag, color):
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], width=2, tags=tag, fill = color)

    def connect_points(self, p1, p2, p3, p4, tag, color):
        self.draw_line(p1, p3, tag, color)
        self.draw_line(p3, p4, tag, color)
        self.draw_line(p2, p4, tag, color)
    
    def middle_point(self, p1, p2):
        m = ( (p1[0]+p2[0])/2 , (p1[1]+p2[1])/2 )
        return m  

    def draw_init(self, event):
        widget = event.widget
        x = widget.canvasx(event.x)
        y = widget.canvasx(event.y)
        
        if self.click_number == 0:
            self.p1 = (x, y)
            self.draw_point(self.p1, "p1")
        elif self.click_number == 1:
            self.p2 = (x, y)
            self.draw_point(self.p2, "p2")
            self.draw_line(self.p1, self.p2, "l12", "red")
        elif self.click_number == 2:
            self.p3 = (x, y)
            self.draw_point(self.p3, "p3")
            canvas.delete("l12")
            self.draw_line(self.p1, self.p3, "l13", "red")
            self.draw_line(self.p2, self.p3, "l23", "red")
        elif self.click_number == 3:
            self.p4 = (x, y)
            self.draw_point(self.p4, "p4")
            canvas.delete("l12"); canvas.delete("l23"); canvas.delete("l13")
            self.connect_points(self.p1, self.p2, self.p3, self.p4, "lines", "red")
            self.draw_bezier(d, self.p1, self.p2, self.p3, self.p4)
            self.click_number += 1

        self.click_number += 1

        self.previous = (x, y)

    def select(self, event):
        if self.click_number > 5:
            widget = event.widget   # Get handle to canvas 
            x = widget.canvasx(event.x)
            y = widget.canvasx(event.y)
            self.item = widget.find_closest(x, y)[0]        # ID for closest
            self.previous = (x, y)

    def drag(self, event):
        widget = event.widget
        x = widget.canvasx(event.x)
        y = widget.canvasx(event.y)

        if self.item < 8:
            canvas.move(self.item, x-self.previous[0], y-self.previous[1])
            if self.item == 1: #p1
                self.p1 = (self.p1[0]+x-self.previous[0], self.p1[1]+y-self.previous[1])
            elif self.item == 2: #p2
                self.p2 = (self.p2[0]+x-self.previous[0], self.p2[1]+y-self.previous[1])
            elif self.item == 4: #p3
                self.p3 = (self.p3[0]+x-self.previous[0], self.p3[1]+y-self.previous[1])
            elif self.item == 7: #p4
                self.p4 = (self.p4[0]+x-self.previous[0], self.p4[1]+y-self.previous[1])
            self.update_canvas()
        
        self.previous = (x, y)

    def update_canvas(self):
        canvas.delete("lines"); canvas.delete("bzcurve")
        self.connect_points(self.p1, self.p2, self.p3, self.p4, "lines", "red")
        self.draw_bezier(d, self.p1, self.p2, self.p3, self.p4)

    def draw_bezier(self, depth, p1, p2, p3, p4):
        if (depth ==0):
            self.connect_points(p1, p2, p3, p4, "bzcurve", "black")
        
        else:
            p13 = self.middle_point(p1, p3)
            p34 = self.middle_point(p3, p4)
            p24 = self.middle_point(p2, p4)
            p134 = self.middle_point(p13, p34)
            p234 = self.middle_point(p34, p24)
            q = self.middle_point(p134, p234)

            depth = depth-1
            self.draw_bezier(depth, p1, q, p13, p134)
            self.draw_bezier(depth, q, p2, p234, p24)
    
# Get an instance of the Bezier object
bc = Bezier()

# Bind mouse events to methods (could also be in the constructor)
canvas.bind("<Button-1>", bc.draw_init)
canvas.bind("<Button-1>", bc.select, add='+')
canvas.bind("<B1-Motion>", bc.drag)

root.mainloop()