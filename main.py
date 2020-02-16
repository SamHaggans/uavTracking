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
master.title("UAV Tracking Simulation")
master.resizable(0, 0)

class Target:
    def __init__(self, canvas, color, starting, width):
        self.canvas = canvas
        self.width = width
        self.color = color
        self.pos = starting
        self.starting = starting
        self.id = canvas.create_rectangle(self.starting[0], self.starting[1], self.starting[0]+width, self.starting[1]+width, fill = self.color)
        self.pos = [self.starting[0]+width/2, self.starting[1]+width/2]
        self.signal = Signal(self, 10000)
        self.heading = 0
    def move(self, x, y):
        self.canvas.move(self.id, x, y)
        self.pos = [self.canvas.coords(self.id)[0]+self.width/2, self.canvas.coords(self.id)[1]+self.width/2]

    def run(self):
        oldPos = self.pos
        seed = random.random()
        head_seed = random.uniform(-10, 10)
        self.heading += head_seed
        done = False
        if seed < 0.15:
            angle = random.uniform(self.heading +0, self.heading +45)
            newx, newy = 1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))
            self.move(newx, newy)
        elif seed < 0.40:
            angle = random.uniform(self.heading +45, self.heading +90)
            newx, newy = 1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))
            self.move(newx, newy)
        elif seed < 0.65:
            angle = random.uniform(self.heading +90, self.heading +135)
            newx, newy = 1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))
            self.move(newx, newy)
        elif seed < 0.8:
            angle = random.uniform(self.heading +135, self.heading +180)
            newx, newy = 1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))
            self.move(newx, newy)
        elif seed < 0.9:
            angle = random.uniform(self.heading +180, self.heading +225)
            newx, newy = 1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))
            self.move(newx, newy)
        else:
            angle = random.uniform(self.heading +315, self.heading +360)
            newx, newy = 1*math.cos(math.radians(angle)), 1*math.sin(math.radians(angle))
            self.move(newx, newy)
        if self.pos[0] > 1450:
            self.move(1450-self.pos[0], 0)
        if self.pos[0] < 50:
            self.move(50-self.pos[0], 0)
        if self.pos[1] > 650:
            self.move(0, 650-self.pos[1])
        if self.pos[1] < 50:
            self.move(0, 50-self.pos[1])
        canvas.create_line(oldPos[0], oldPos[1], self.pos[0], self.pos[1], fill="orange red")
class UAV:
    def __init__(self, canvas, color, starting, width):
        self.canvas = canvas
        self.width = width
        self.color = color
        self.pos = starting
        self.starting = starting
        self.id = canvas.create_rectangle(self.starting[0], self.starting[1], self.starting[0]+width, self.starting[1]+width, fill = self.color)
        self.pos = [self.starting[0]+width/2, self.starting[1]+width/2]
        self.tracks = []
        self.trackCount = 0
        self.guess = [500, 500]
        self.badGuess = 0
    def move(self, x, y):
        self.canvas.move(self.id, x, y)
        self.pos = [self.canvas.coords(self.id)[0]+self.width/2, self.canvas.coords(self.id)[1]+self.width/2]
    def getPos(self):
        return self.pos

    def getSignalStrength(self, signal):
        return signal.getStrength(self.pos)
    
    def circle(self, x1, y1):
        selfx = self.pos[0]
        selfy = self.pos[1]

        x, y = selfx-x1, selfy-y1
        angle = 0

        if x == 0:
            if y > 0:
                angle = -90
            else:
                angle = 90
        if y == 0:
            if x > 0:
                angle = 0
            else:
                angle = 180
        if x > 0 and y < 0:
            angle = 90-math.degrees(-atan(x/y))
        if x < 0 and y < 0:
            angle = math.degrees(atan(x/y))+90
        if x > 0 and y > 0:
            angle = -90-math.degrees(-atan(x/y))
        if x < 0 and y > 0:
            angle = math.degrees(atan(x/y))-90
        
        movex = sin(math.radians(angle))
        movey = cos(math.radians(angle))
        self.move(movex, movey)

    def track1(self, signal):
        def searchBounds(bounds, cir1, cir2, cir3, interval):
            bestx, besty = bounds[0], bounds[1]
            x = bounds[0]
            y = bounds[1]
            minDist = 10000000000
            while x <= bounds[2]:
                while y <= bounds[3]:
                    dist1 = pointToCircle(x, y, cir1[1], cir1[2], cir1[0])
                    dist2 = pointToCircle(x, y, cir2[1], cir2[2], cir2[0])
                    dist3 = pointToCircle(x, y, cir3[1], cir3[2], cir3[0])
                    curDist = dist1+dist2+dist3
                    if curDist < minDist:
                        minDist = curDist
                        bestx = x
                        besty = y
                    y+= interval
                x += interval
            posMinx = bestx - interval
            posMaxx = bestx + interval
            posMiny = besty - interval
            posMaxy = besty + interval
            if interval < 0.5:
                return [x,y]
            else:
                return(searchBounds([posMinx, posMiny, posMaxx, posMaxy], cir1, cir2, cir3, interval/2))
    

        strength = self.getSignalStrength(signal)
        distance = math.sqrt(10000/strength)
        self.tracks.append([distance, self.pos[0], self.pos[1]])
        if self.trackCount >= 2:
            oldGuess = self.guess
            x1, y1, x2, y2 = formulas.getBounds([self.tracks[self.trackCount-2], self.tracks[self.trackCount-1], self.tracks[self.trackCount]])
            self.guess = formulas.searchBounds([x1, y1, x2, y2], self.tracks[self.trackCount-2], self.tracks[self.trackCount-1], self.tracks[self.trackCount], 10)
            if self.trackCount > 5:
                if formulas.distance(self.guess[0], self.guess[1], oldGuess[0], oldGuess[1]) > 15.0:
                    self.badGuess += 1
                if self.badGuess < 10:
                    self.guess = oldGuess
                else:
                    self.badGuess = 0
            canvas.create_rectangle(self.guess[0]-2.5, self.guess[1]-2.5, self.guess[0]+2.5, self.guess[1]+2.5, fill = "blue")
        self.trackCount += 1


    
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

def create_circle(x, y, r):
    canvas.create_oval(x-r, y-r, x+r, y+r)

def animation(width, height):
    canvas.create_rectangle(0,0,80,80)
    target = Target(canvas, "red", [width/2, height/2], 10)
    drone = UAV(canvas, "blue", [500, 300], 10)
    canvas.create_rectangle(1225, 5, 1495, 200, fill = "white")
    canvas.create_text(1250, 10, anchor="nw", text = "Simulation Information: ")
    target_real = canvas.create_text(1250, 25, anchor="nw", text = "Target Position: ("+str(round(target.pos[0], 2))+", "+str(round(target.pos[1], 2))+")")
    uav_real = canvas.create_text(1250, 40, anchor="nw", text = "UAV Position: ("+str(round(drone.pos[0], 2))+", "+str(round(drone.pos[1], 2))+")")
    sig_strength = canvas.create_text(1250, 55, anchor="nw", text = "Signal Strength: ("+str(round(drone.getSignalStrength(target.signal), 6))+")")
    master.update_idletasks()#needed tkinter things
    master.update()
    count = 0
    while True:
        count += 1
        
        canvas.itemconfig(target_real, text = "Target Position: ("+str(round(target.pos[0],2))+", "+str(round(target.pos[1],2))+")")
        canvas.itemconfig(uav_real, text = "UAV Position: ("+str(round(drone.pos[0], 2))+", "+str(round(drone.pos[1], 2))+")")
        canvas.itemconfig(sig_strength, text = "Signal Strength: ("+str(round(drone.getSignalStrength(target.signal), 6))+")")
        strength = drone.getSignalStrength(target.signal)
        distance = math.sqrt(10000/strength)

        canvas.create_rectangle(400,400,410,410)
        drone.circle(400, 400)
        print(formulas.distance(drone.pos[0], drone.pos[1], 400, 400))
        #target.run()
        #drone.track1(target.signal)
        #create_circle(drone.pos[0], drone.pos[1], distance)
        time.sleep(0.03)
        master.update_idletasks()#needed tkinter things
        master.update()
        
animation(canvas_width, canvas_height)
mainloop()

