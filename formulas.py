import math
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

def searchBounds(bounds, cir1, cir2, cir3, interval):
    bestx, besty = bounds[0], bounds[1]
    x = bounds[0]
    y = bounds[1]
    minDist = 10000000000
    while x <= bounds[2]:
        y = bounds[1]
        while y <= bounds[3]:
            dist1 = pointToCircle(x, y, cir1[1], cir1[2], cir1[0])
            dist2 = pointToCircle(x, y, cir2[1], cir2[2], cir2[0])
            dist3 = pointToCircle(x, y, cir3[1], cir3[2], cir3[0])
            curDist = dist1+dist2+dist3
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
        return(searchBounds([posMinx, posMiny, posMaxx, posMaxy], cir1, cir2, cir3, interval/2))

x1, y1, x2, y2 = getBounds([[5, 0, 0], [5, 10, 0], [5, 5, 100]])

print(searchBounds([x1, y1, x2, y2], [5, 0, 0], [5, 10, 0], [5, 5, 100], 5))

    