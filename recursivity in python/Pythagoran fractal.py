#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is an interactive implementation of a Pythagorean fractal, a plane fractal constructed from squares, using the tkinter package in python
Reference: https://steemit.com/fractal/@fractal-team/create-a-pythagorean-tree-using-python
"""

import tkinter as tk
import numpy as np

root = tk.Tk()
canvas = tk.Canvas(root, width=700, height=500)

root.title("Pythagorean fractal")

canvas.grid(row=0, column=0, columnspan = 7)
frame = tk.Frame(root).grid(row=0, column=0, sticky="n", columnspan = 7)

l = 100     #biggest square side
max_depth = 6

# we find value of alfa according to the ratio 
alfa1 = np.arcsin(3/5)  #3:4:5
alfa2 = np.arcsin(5/13) #5:12:13

fi = np.pi/2  #initial square rotation (90 deg)

class Pythagorean():
    def __init__(self):
        self.p0 = (400, 450)
        
        self.level = 0
        self.alfa = alfa1
        
        self.level_label = tk.Label(root, text="Level")
        self.level_label.config(font =("Courier", 14))
        self.current_level = tk.IntVar(value=6)
        self.level_spinbox = tk.Spinbox(root, from_=0, to=max_depth, 
                                        textvariable=self.current_level, 
                                        command=self.parameters_changed, font=20)
        
        self.ratio_label = tk.Label(root, text="Ratio")
        self.ratio_label.config(font =("Courier", 14))
        self.current_ratio = tk.DoubleVar(value=self.alfa)
        self.ratio_r1 = tk.Radiobutton(root, text="3:4:5", variable=self.current_ratio, value=alfa1, 
                                       command=self.parameters_changed, font=20)
        self.ratio_r2 = tk.Radiobutton(root, text="5:12:13", variable=self.current_ratio, value=alfa2, 
                                       command=self.parameters_changed, font=20)
        
        self.level_label.grid(row=1, column=3, sticky=tk.W, pady=2)
        self.level_spinbox.grid(row =1, column=4, sticky=tk.W, pady=2)
        self.ratio_label.grid(row=2, column=3, sticky=tk.W, pady=2, rowspan=2)
        self.ratio_r1.grid(row=2, column=4, sticky=tk.W, pady=2)
        self.ratio_r2.grid(row=3, column=4, sticky=tk.W, pady=2)

        self.parameters_changed()


    def parameters_changed(self):
        canvas.delete("all")
        self.level = self.current_level.get()
        self.alfa = self.current_ratio.get()
        self.evolve(self.level,self.p0, l, fi, self.alfa)
        

    def evolve(self, level, p0, l, fi, alfa):

        dx = l * np.sin(fi) 
        dy = l * np.cos(fi)
            
        p1 = (p0[0]+dx, p0[1]-dy)
        p2 = (p0[0]+dx-dy, p0[1]-dy-dx)
        p3 = (p0[0]-dy, p0[1]-dx)
        p4 = (p0[0]-dy+l*np.cos(alfa)*np.sin(fi-alfa), p0[1]-dx-l*np.cos(alfa)*np.cos(fi-alfa) )
            

        color="#"+str((max_depth+1-level)*15)+"0438" if level>1 else "#900438"
       
        canvas.create_polygon(p0[0], p0[1],
                              p1[0], p1[1],
                              p2[0], p2[1],
                              p3[0], p3[1], fill=color)
        
        if (level !=0):
            self.evolve(level-1, p4, l*np.sin(alfa), fi-alfa+np.pi/2, alfa)
            self.evolve(level-1, p3, l*np.cos(alfa), fi-alfa, alfa)
            

p = Pythagorean()
root.mainloop()
