from tkinter import *
import time
import math
from math import sin, cos, tan, asin, acos, atan
import formulas
import random

master = Tk()

canvas_width = 1500
canvas_height = 700
canvas = Canvas(master, 
           width=canvas_width,
           height=canvas_height)

canvas.pack()
master.title("UAV Tracking Simulation")#title
master.resizable(0, 0)#stay size always
master.wm_attributes("-topmost", 1)#topmost window

y = int(canvas_height / 2)

class Target:
    def __init__(self, canvas, color, starting, width):
        self.canvas = canvas
        self.width = width
        self.color = color
        self.pos = starting
        self.starting = starting
        self.id = canvas.create_rectangle(self.starting[0], self.starting[1], self.starting[0]+width, self.starting[1]+width, fill = self.color)
        self.pos = [self.starting[0]+width/2, self.starting[1]+width/2]
        self.signal = Signal(self, 100)
    def move(self, x, y):
        self.canvas.move(self.id, x, y)
        self.pos = [self.canvas.coords(self.id)[0]+self.width/2, self.canvas.coords(self.id)[1]+self.width/2]

    def run(self):
        seed = random.random()
        done = False
        if seed < 0.15:
            angle = random.uniform(0, 45)
            newx, newy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
            self.move(newx, newy)
        elif seed < 0.40:
            angle = random.uniform(45, 90)
            newx, newy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
            self.move(newx, newy)
        elif seed < 0.65:
            angle = random.uniform(90, 135)
            newx, newy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
            self.move(newx, newy)
        elif seed < 0.8:
            angle = random.uniform(135, 180)
            newx, newy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
            self.move(newx, newy)
        elif seed < 0.9:
            angle = random.uniform(180, 225)
            newx, newy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
            self.move(newx, newy)
        else:
            angle = random.uniform(315, 360)
            newx, newy = math.cos(math.radians(angle)), math.sin(math.radians(angle))
            self.move(newx, newy)

class UAV:
    def __init__(self, canvas, color, starting, width):
        self.canvas = canvas
        self.width = width
        self.color = color
        self.pos = starting
        self.starting = starting
        self.id = canvas.create_rectangle(self.starting[0], self.starting[1], self.starting[0]+width, self.starting[1]+width, fill = self.color)
        self.pos = [self.starting[0]+width/2, self.starting[1]+width/2]
    def move(self, x, y):
        self.canvas.move(self.id, x, y)
        self.pos = [self.canvas.coords(self.id)[0]+self.width/2, self.canvas.coords(self.id)[1]+self.width/2]
    def getPos(self):
        return self.pos

    def getSignalStrength(self, signal):
        return signal.getStrength(self.pos)

    
class Signal:
    def __init__(self, source, power):
        self.source = source
        self.power = power
    def getStrength(self, pos):
        x = pos[0]
        y = pos[1]
        
        distance = formulas.distance(x, y, self.source.pos[0], self.source.pos[1])

        returnPower = self.power/distance**2
        return returnPower


def animation(width, height):
    target = Target(canvas, "red", [width/2, height/2], 10)
    drone = UAV(canvas, "blue", [0, 0], 10)
    
    master.update_idletasks()#needed tkinter things
    master.update()
    while True:
        #target.run()
        master.update_idletasks()#needed tkinter things
        master.update()
mainloop()
animation(canvas_width, canvas_height)
