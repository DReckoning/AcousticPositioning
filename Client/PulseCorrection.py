# this will correct missing or false pulses.


def process(rocks,syncs,nn):
    # checker
    for n in range(nn):
        rockavg = 0
        for s in rocks[n]:
            rockavg+= float(s)/float(len(rocks[n]))
        lastsamp = 0
        i = 0

        print 'avg ',rockavg

        for s in rocks[n]:
            i = i+1
            if (lastsamp == 0):
                lastsamp = s
            else:
                if (((s - lastsamp) - rockavg)>0.25):
                    print '\nRock Error on node ',n,' sample ',i
                lastsamp = s

    # checker2
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

    return [newrocks,newsyncs]