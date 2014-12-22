import fastSpatial as spatial
import numpy
import Sync
from SensorLocations import * 
import matplotlib.pyplot as plt


# This module will process a set of data. It will read from files and process the data.

def run():

    nodeinit()

    nn = len(Nodes)
    
    syncs = []
    rocks = []

    # pull from file
    for n in range(nn):
        filename = 's'+str(n)+'.txt'
        f = open(filename, 'r')
        srocks = f.readline()
        ssyncs = f.readline()
        sensorRocks = []
        sensorSyncs = []
        strin = ''
        
        for c in srocks:
            if (c == ','):
                sensorRocks.append(float(strin))
                strin = ''
            else:
                strin+=c

        strin = ''

        for c in ssyncs:
            if (c == ','):
                sensorSyncs.append(float(strin))
                strin = ''
            else:
                strin+=c

        syncs.append(sensorSyncs)
        rocks.append(sensorRocks)

    #checker
    for n in range(nn):
        rockavg = 0
        for s in rocks[n]:
            rockavg+= float(s)/float(len(rocks[n]))
        lastsamp = 0
        i = 0
        for s in rocks[n]:
            i = i+1
            if (lastsamp == 0):
                lastsamp = s
            else:
                if (((s - lastsamp) - rockavg)>0.25):
                    print '\nRock Error on node ',n,' sample ',i
                lastsamp = s

    #checker2
    for n in range(nn):
        rockavg = 0
        for s in syncs[n]:
            rockavg+= float(s)/float(len(syncs[n]))
        lastsamp = 0
        i = 0
        for s in syncs[n]:
            i = i+1
            if (lastsamp == 0):
                lastsamp = s
            else:
                if (((s - lastsamp) - rockavg)>0.25):
                    print '\nRock Error on node ',n,' sample ',i
                lastsamp = s


    minrocks = 999
    minsyncs = 999

    newsyncs = []
    newrocks = []


    for n in range(nn):
        if (minrocks > len(rocks[n])):
            minrocks = len(rocks[n])
            
        if (minsyncs > len(syncs[n])):
            minsyncs = len(syncs[n])
    print '\nHACKING OFF'       
    for n in range(nn):

        thisnodesrocks = []

        thisnodessyncs = []


        for i in range(minrocks):
            thisnodesrocks.append(rocks[n][i])

        for i in range(minsyncs):
            thisnodessyncs.append(syncs[n][i])

        newsyncs.append(thisnodessyncs)

        newrocks.append(thisnodesrocks)

        print len(rocks[n]) - len(thisnodesrocks)
        print len(syncs[n]) - len(thisnodessyncs)
        
    syncs = newsyncs

    rocks = newrocks

    SyncedRockTimes = Sync.process(Nodes,SyncNode[0],rocks,syncs,333)

    position = []

    spots = len(SyncedRockTimes[0])


    if nn == 4:
        worsteSensor = []

        for spot in range(0,spots):
            smallestError = 999
            worsteSensor.append(0)
            for x in range(0,4):
                for n in range(0,nn):
                    Nodes[n].setDelay(SyncedRockTimes[n][spot])
                    
                threeNodes = []
                for j in range(0,4):
                    if j != x:
                        threeNodes.append(Nodes[j])
                test1 = spatial.process(threeNodes,0,333,30,5)
                if test1.err < smallestError:
                    smallestError = test1.err
                    worsteSensor[spot] = x
                    bestTest = test1
            if smallestError < 0.1:
                position.append(bestTest)
                #print bestTest

        print '\nFinal DATA'
        for test in position:
            print test

        plt.hist(worsteSensor)
        plt.show()

    elif nn == 3:
        for spot in range(0,spots):
            Nodes[n].setDelay(SyncedRockTimes[n][spot])
                    
            test1 = spatial.process(threeNodes,0,333,30,5)
                
            if test1 < 0.1:
                position.append(bestTest)

        print '\nFinal DATA'
        for test in position:
            print test
    else:
        print 'Error! Using a non-developed number of sensors: ', nn


    
    posx = []
    posy = []
    f = open('results.csv', 'w')
    f.write('time, x, y\n')
    for pos in position:
        line = str(pos.time) + ', ' + str(pos.x) + ', ' + str(pos.y) +'\n'
        f.write(line)
        posx.append(pos.x)
        posy.append(pos.y)

    plt.scatter(posx, posy)
    plt.axis([-3, 10,-1, 5])
    plt.show()

run()
