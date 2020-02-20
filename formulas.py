import math
from math import sin, cos, tan, acos, asin, atan
def distance(x1, y1, x2, y2):
    value = abs(math.sqrt((x2-x1)**2+(y2-y1)**2))
    if value < 1:
        return 1
    else:
        return value
def midpoint(x1, y1, x2, y2):
    midx = (x1+x2)/2
    midy = (y1+y2)/2
    return [midx, midy]

def pointToCircle(px, py, cx, cy, r):
    distanceVal = distance(px, py, cx, cy)
    return abs(distanceVal-r)

def getBounds(array):
        minx = 10000000
        maxx = -10000000
        miny = 10000000
        maxy = -10000000
        x = 0
        y = 0
        r = 0
        for i in range(len(array)):
            x = array[i][1]
            y = array[i][2]
            r = array[i][0]
            posMinx = x - r
            posMaxx = x + r
            posMiny = y - r
            posMaxy = y + r
            if posMinx < minx:
                minx = posMinx
            if posMaxx > maxx:
                maxx = posMaxx
            if posMiny < miny:
                miny = posMiny
            if posMaxy > maxy:
                maxy = posMaxy
        return minx, miny, maxx, maxy

def searchBounds(bounds, circles, interval):
    bestx, besty = bounds[0], bounds[1]
    x = bounds[0]
    y = bounds[1]
    minDist = 10000000000
    while x <= bounds[2]:
        y = bounds[1]
        while y <= bounds[3]:
            curDist = 0
            for cir in circles:
                curDist += pointToCircle(x, y, cir[1], cir[2], cir[0])
            if curDist < minDist:
                minDist = curDist
                bestx = x
                besty = y
            if minDist == 0:
                return [bestx, besty]
            y += interval
        x += interval
        
    posMinx = bestx - interval
    posMaxx = bestx + interval
    posMiny = besty - interval
    posMaxy = besty + interval
    if interval < 0.001:
        return [bestx,besty]
    else:
        return(searchBounds([posMinx, posMiny, posMaxx, posMaxy], circles, interval/2))

def getAngle(px, py, tx, ty):
    x, y = px-tx, py-ty
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
    
    return angle

def getAverage(pointArray):
    lenInit = len(pointArray)
    points = pointArray
    sumx = 0
    sumy = 0 
    for point in points:
        sumx += point[0]
        sumy += point[1]
    avgx = sumx / len(points)
    avgy = sumy / len(points)

    toDelete = []
    for i in range(len(points)-1):
        if (distance(points[i][0], points[i][1], avgx, avgy))**2 > 5000:
            toDelete.append(points[i])
    for i in toDelete:
        del i
    if lenInit == len(points):
        return [avgx, avgy]
    else:
        return getAverage(points)
