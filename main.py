from tkinter import *
import csv
import time
import math
from math import sin, cos, tan, asin, acos, atan
import formulas
import random

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
        canvas = self.canvas
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
        self.guesses = [[500,500]]
        self.badGuess = 0
        self.moveCount = 0
        self.constrain = True
    def move(self, x, y):
        self.canvas.move(self.id, x, y)
        self.pos = [self.canvas.coords(self.id)[0]+self.width/2, self.canvas.coords(self.id)[1]+self.width/2]
        self.moveCount +=1
    def getPos(self):
        return self.pos

    def getSignalStrength(self, signal):
        return signal.getStrength(self.pos)
    
    def circle(self, x1, y1):

        angle = formulas.getAngle(self.pos[0], self.pos[1], x1, y1)
        movex = sin(math.radians(angle))*2
        movey = cos(math.radians(angle))*2
        self.move(movex, movey)

    def track1(self, signal, moveCountSearch, circlesCountInit, cirDist):
        canvas = self.canvas
        strength = self.getSignalStrength(signal)
        distance = math.sqrt(10000/strength)
        if self.moveCount % moveCountSearch == 0:
            self.tracks.append([distance, self.pos[0], self.pos[1]])
            if self.trackCount >= circlesCountInit:
                cirCount = circlesCountInit
                circles = []
                for i in range(cirCount):
                    circles.append(self.tracks[self.trackCount-i])

                x1, y1, x2, y2 = formulas.getBounds(circles)

                self.guess = formulas.searchBounds([x1, y1, x2, y2], circles, 10)
                if self.badGuess > 10:
                    self.constrain = False
                if len(self.guesses) > 5:
                    pointCount = 5
                    avgPoints = []
                    for i in range(pointCount):
                        avgPoints.append(self.guesses[len(self.guesses)-1-i])

                    lastNAvg = formulas.getAverage(avgPoints)
                    if formulas.distance(self.guess[0],self.guess[1], lastNAvg[0], lastNAvg[1]) < 100:
                        self.guesses.append(self.guess)
                    else:
                        self.badGuess +=1
                        self.guess = self.guesses[len(self.guesses)-1]
                else:
                    if (self.badGuess > 0):
                        self.badGuess -= 1
                        if self.badGuess == 0:
                            self.constrain = True
                    self.guesses.append(self.guess)
                canvas.create_rectangle(self.guess[0]-2.5, self.guess[1]-2.5, self.guess[0]+2.5, self.guess[1]+2.5, fill = "orange")
            self.trackCount += 1

        if distance > cirDist:
            if len(self.guesses) > 10:
                pointCount = 5
                avgPoints = []
                for i in range(pointCount):
                    avgPoints.append(self.guesses[len(self.guesses)-1-i])

                lastNAvg = formulas.getAverage(avgPoints)
                curAngle = formulas.getAngle(self.pos[0],self.pos[1], lastNAvg[0], lastNAvg[1])
            else:
                curAngle = formulas.getAngle(self.pos[0],self.pos[1], self.guess[0], self.guess[1])
            
            sinAngle = 45*sin(distance/2)
            movAngle = curAngle + sinAngle

            self.move(-2*cos(math.radians(movAngle)), 2*sin(math.radians(movAngle)))
        else:
            if len(self.guesses) > 10:
                pointCount = 5
                avgPoints = []
                for i in range(pointCount):
                    avgPoints.append(self.guesses[len(self.guesses)-1-i])

                lastNAvg = formulas.getAverage(avgPoints)
                self.circle(lastNAvg[0], lastNAvg[1])
            else:
                self.circle(self.guess[0], self.guess[1])
            

    
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

def animation(width, height, circles, moves, dist):
    master = Tk()
    canvas = Canvas(master, 
           width=width,
           height=height)

    canvas.pack()
    master.title("UAV Tracking Simulation")
    master.resizable(0, 0)
    target = Target(canvas, "red", [width/2, height/2], 10)
    drone = UAV(canvas, "blue", [300, 200], 10)
    canvas.create_rectangle(1225, 5, 1495, 200, fill = "white")
    canvas.create_text(1250, 10, anchor="nw", text = "Simulation Information: ")
    target_real = canvas.create_text(1250, 25, anchor="nw", text = "Target Position: ("+str(round(target.pos[0], 2))+", "+str(round(target.pos[1], 2))+")")
    uav_real = canvas.create_text(1250, 40, anchor="nw", text = "UAV Position: ("+str(round(drone.pos[0], 2))+", "+str(round(drone.pos[1], 2))+")")
    sig_strength = canvas.create_text(1250, 55, anchor="nw", text = "Signal Strength: ("+str(round(drone.getSignalStrength(target.signal), 6))+")")
    master.update_idletasks()
    master.update()
    count = 0
    loopMax = 8000
    loopCount = 0
    writeCount = 0
    oldGuess = [0,0]
    while loopCount < loopMax:
        count += 1
        loopCount +=1
        canvas.itemconfig(target_real, text = "Target Position: ("+str(round(target.pos[0],2))+", "+str(round(target.pos[1],2))+")")
        canvas.itemconfig(uav_real, text = "UAV Position: ("+str(round(drone.pos[0], 2))+", "+str(round(drone.pos[1], 2))+")")
        canvas.itemconfig(sig_strength, text = "Signal Strength: ("+str(round(drone.getSignalStrength(target.signal), 6))+")")
        strength = drone.getSignalStrength(target.signal)
        distance = math.sqrt(10000/strength)

        target.run()
        drone.track1(target.signal, moves, circles, dist)
        
        if len(drone.guesses) > 3 and loopCount > 30:
            if drone.guess != oldGuess:
                actualDistance = formulas.distance(drone.guess[0], drone.guess[1], target.pos[0], target.pos[1])
                
                #filey = open('goatgoose.csv','a')
                #csvwriter = csv.writer(filey, delimiter=',',
                                #quotechar='|', quoting=csv.QUOTE_MINIMAL)
                #csvwriter.writerow([writeCount, actualDistance])
                #filey.close() 
            writeCount +=1
            oldGuess = drone.guess
        time.sleep(0.02)
        master.update_idletasks()
        master.update()
    master.destroy()
canvas_width = 1500
canvas_height = 700


animation(canvas_width, canvas_height, 6, 5, 100)

