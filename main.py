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
            newx, newy = random.uniform(-1,1), random.uniform(-1,1)
            while done != True:
                if math.degrees(atan(math.radians(newx/newy))) <= 45:
                    self.move(newx, newy)
                    done = True
                else:
                    newx, newy = random.uniform(-1,1), random.uniform(-1,1)
        elif seed < 0.40:
            newx, newy = random.uniform(-1,1), random.uniform(-1,1)
            while done != True:
                if math.degrees(atan(math.radians(newx/newy))) >= 45 and math.degrees(atan(math.radians(newx/newy))) <= 90:
                    self.move(newx, newy)
                    done = True
                else:
                    newx, newy = random.uniform(-1,1), random.uniform(-1,1)
        elif seed < 0.65:
            newx, newy = random.uniform(-1,1), random.uniform(-1,1)
            while done != True:
                if math.degrees(atan(math.radians(newx/newy))) >= 90 and math.degrees(atan(math.radians(newx/newy))) <= 135:
                    self.move(newx, newy)
                    done = True
                else:
                    newx, newy = random.uniform(-1,1), random.uniform(-1,1)
        elif seed < 0.8:
            newx, newy = random.uniform(-1,1), random.uniform(-1,1)
            while done != True:
                if math.degrees(atan(math.radians(newx/newy))) >= 135 and math.degrees(atan(math.radians(newx/newy))) <= 180:
                    self.move(newx, newy)
                    done = True
                else:
                    newx, newy = random.uniform(-1,1), random.uniform(-1,1)
        elif seed < 0.9:
            newx, newy = random.uniform(-1,1), random.uniform(-1,1)
            while done != True:
                if math.degrees(atan(math.radians(newx/newy))) >= 180 and math.degrees(atan(math.radians(newx/newy))) <= 225:
                    self.move(newx, newy)
                    done = True
                else:
                    newx, newy = random.uniform(-1,1), random.uniform(-1,1)
        else:
            newx, newy = random.uniform(-1, 1), random.uniform(-1, 1)
            while done != True:
                if math.degrees(atan(math.radians(newx/newy))) >= 315 and math.degrees(atan(math.radians(newx/newy))) <= 360:
                    self.move(newx, newy)
                    done = True
                else:
                    newx, newy = random.uniform(-1, 1), random.uniform(-1, 1)

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
    print(drone.getSignalStrength(target.signal))
    drone.move(750,350)
    print(drone.getSignalStrength(target.signal))
    print(random.uniform(-1, 1))
    while True:
        print("here")
        target.run()
        time.sleep(1)
animation(canvas_width, canvas_height)
mainloop()