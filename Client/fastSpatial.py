from __future__ import division
import numpy as np
import matplotlib.pylab as plt
from pylab import *
#import mpl_toolkits.mplot3d.axes3d

resolution = 10
scale = 7
narrowing = 3

class Node(object):
    def __init__(self,x,y,h):
        self.x = x
        self.y = y
        self.h = h

    def __str__(self):
        return "x%d,y%d,h%d,delay%d" % (self.x,self.y,self.h,self.delay)

    def posSet(self,x,y,h):
        self.x = x
        self.y = y
        self.h = h
    
    def setDelay(self,delay):
        self.delay = delay
        
    def dist(self,otherNode):
        dx = otherNode.x - self.x
        dy = otherNode.y - self.y
        dh = otherNode.h - self.h
        sx = np.square(dx)
        sy = np.square(dy)
        sh = np.square(dh)
        return np.sqrt((sx+sy+sh))

    def dist(self,x,y,h):
        dx = x - self.x
        dy = y - self.y
        dh = h - self.h
        sx = np.square(dx)
        sy = np.square(dy)
        sh = np.square(dh)
        return np.sqrt((sx+sy+sh))

    def TimeDist(self,x,y,h,speed):
        dx = x - self.x
        dy = y - self.y
        dh = h - self.h
        sx = np.square(dx)
        sy = np.square(dy)
        sh = np.square(dh)
        return (np.sqrt((sx+sy+sh)))/speed

class Position(object):
    def __init__(self,time,x,y,error):
        self.x = x
        self.y = y
        self.time = time
        self.err = error
    def __str__(self):
        return "Rock at %.2f sec: x(%.3f),y(%.3f)" % (self.time,self.x,self.y)
    def x(self):
        return self.x
    def y(self):
        return self.y

def findDelay(Nodes,x,y,h,speed):
    zero = Nodes[0].TimeDist(x,y,h,speed)
    for node in Nodes:
        node.delay = node.TimeDist(x,y,h,speed) - zero    

def findCenter(Nodes):
    lowestX = Nodes[0].x
    highestX = Nodes[0].x
    lowestY = Nodes[0].y 
    highestY = Nodes[0].y
    for node in Nodes:
        if node.x < lowestX:
            lowestX = node.x

        if node.x > highestX:
            highestX = node.x

        if node.y < lowestY:
            lowestY = node.y

        if node.y > highestY:
            highestY = node.y

    centerX = (highestX+lowestX)/float(2)
    centerY = (highestY+lowestY)/float(2)
    return centerX, centerY

    
def getError(Nodes,x,y,h,speed):
    error = 0
    zero = Nodes[0].TimeDist(x,y,h,speed)
    for node in Nodes:
        PredictedDelay = node.TimeDist(x,y,h,speed) - zero
        error = error + np.square(node.delay - PredictedDelay)
            
    return np.sqrt(error)

def process(Nodes, height, speed,xr,yr):
    numNodes = len(Nodes)
    #zero out node0's delay
    zero = Nodes[0].delay
    for node in Nodes:
         node.setDelay(node.delay - zero)
         
    Nodes[0].getDelay = 0
    
    #get the compute area
    [centerX, centerY] = findCenter(Nodes)

#    print '\n CX ',centerX, 'CY ',centerY
    errors = np.zeros((resolution,resolution))
    
    for s in range(scale):
        leasterror = 9999
        for x in range(resolution):
            xpos = centerX + (xr*(x/(resolution-1)) - xr/2)
            for y in range(resolution):
                ypos = centerY + (yr*y/(resolution-1) - yr/2)
                #print '\nx',xpos,' y',ypos
                error = speed*getError(Nodes,xpos,ypos,height,speed)
                if error < leasterror:
                    leasterror = error
                    bestPosx = xpos
                    bestPosy = ypos
                    
                errors[x,y] = error
                
        centerX = bestPosx
        centerY = bestPosy
        xr = xr/narrowing
        yr = yr/narrowing

#        figure(1)
#        imshow(errors)
#        colorbar()
#        grid(True)
#        show()
    #print '\nx',bestPosx,' y',bestPosy               

    pos = Position(zero,bestPosx,bestPosy,leasterror)
    return pos
    


