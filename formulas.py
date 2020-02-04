import math
def distance(x1, y1, x2, y2):
    value = abs(math.sqrt((x2-x1)**2+(y2-y1)**2))
    if value < 1:
        return 1
    else:
        return value