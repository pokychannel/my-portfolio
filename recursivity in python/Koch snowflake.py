#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is an interactive implementation of a half Koch snowflake, a fractal curve, using the tkinter package in python
"""

from tkinter import *
import numpy as np

root = Tk()
canvas = Canvas(root, width=400, height=300)
canvas.pack()

level_label = Label(root, text = "Level")
level_label.config(font =("Courier", 14))


number_label = Label(root, text = "Number")
number_label.config(font =("Courier", 14))


class koch():
    def __init__(self):
        self.p0 = (350, 250); self.p1 = (50, 250)
        self.level =0; self.number=0
        self.sin = 0; self.cos=0

        self.current_level = IntVar(value=0)
        self.level_spinbox = Spinbox(root, from_=0, to=6,
                            textvariable=self.current_level,
                            command=self.parameters_changed, font=20)
        level_label.pack()
        self.level_spinbox.pack(pady=20) 
       
        self.current_number = IntVar(value=3)
        self.number_spinbox = Spinbox(root, from_=3, to=6,
                            textvariable=self.current_number,
                            command=self.parameters_changed, font=20)
        number_label.pack()
        self.number_spinbox.pack(pady=20) 

        self.parameters_changed()
    
    def draw_line(self, p0, p1):
        canvas.create_line(p0[0], p0[1], p1[0], p1[1], width=1)

    def get_sin_cos(self, number):
        self.sin = np.sin(np.deg2rad((number-2)*180/number))
        self.cos = np.cos(np.deg2rad((number-2)*180/number))

    def parameters_changed(self):
        canvas.delete("all")

        self.number=self.current_number.get()
        self.level=self.current_level.get()
        self.get_sin_cos(self.number)

        self.evolve(self.level,self.number,self.p0, self.p1)
    
    def evolve(self, level, number, p0, p1):
        if (level == 0):
            self.draw_line(p0, p1)
        else:
            pa, pb = trisec(p0, p1)
            newpoints = self.rotpi(number, p0, pa, pb, p1)

            for i in range(len(newpoints)-1):
                self.evolve(level-1, number, newpoints[i], newpoints[i+1])

    def rotpi(self, number, p0, pa, pb, p1):
        newpoints = []
        newpoints.extend([p0, pa])

        pivot_point = pa
        rot_point = pb

        for i in range (number-1):
            newpoint = (self.cos*(rot_point[0]-pivot_point[0]) - self.sin*(rot_point[1]-pivot_point[1]) + pivot_point[0],
            self.sin*(rot_point[0]-pivot_point[0]) + self.cos*(rot_point[1]-pivot_point[1]) + pivot_point[1])
            newpoints.extend([newpoint])
            rot_point = pivot_point
            pivot_point = newpoint

        newpoints.extend([pb,p1])

        return newpoints

def trisec(p0, p1):
    pa = (2*p0[0]+p1[0])/3.0, (2*p0[1]+p1[1])/3.0
    pb = (p0[0]+2*p1[0])/3.0, (p0[1]+2*p1[1])/3.0
    return pa, pb

k = koch()
root.mainloop()
