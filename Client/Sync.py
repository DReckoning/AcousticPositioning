#make sure that the first pulse is the first pulse is the same.

# sync rec time - sensor delay due to dist - sync0 rec time + sensor0 delay due to dist.

import fastSpatial as spatial
import matplotlib.pyplot as plt

def process(Nodes,SyncNode,rocks,syncs,speed):
    #get the delay for each node from the sync
    spatial.findDelay(Nodes,SyncNode.x,SyncNode.y,SyncNode.h,speed)

    newData = []

    node0Syncs = syncs[0]

    nn = len(Nodes)
    
    for n in range(0,nn):
        newNodeData = []
        DiD0 = []

        nodeSyncs = syncs[n]
        ns = len(nodeSyncs)
        
        nodeData = rocks[n]
        nr = len(nodeData)

        # find the delays
        averageNodeDelay = 0
        for i in range(0,ns):
            internalDelay = nodeSyncs[i] - Nodes[n].delay - node0Syncs[i] + Nodes[0].delay
            DiD0.append(internalDelay)
            averageNodeDelay += internalDelay/ns

        #plt.plot(DiD0)
        #plt.show()

        # give everything at least the average node delay
        for j in range(0,nr):
            firstRunData  = nodeData[j] - averageNodeDelay
            newNodeData.append(firstRunData)
        
        #fine detail syncing for each sync pulse.
        for i in range(0,ns):
            if i != ns-1: 
                for j in range(0,nr):
                    # if the data is after this sync and before the next.
                    if nodeData[j] > nodeSyncs[i] and nodeData[j] < nodeSyncs[i+1]:
                        newNodeData[j] = nodeData[j]-DiD0[i]
                        
            else: 
                for j in range(0,nr):
                    # if the data is after the last sync
                    if nodeData[j] > nodeSyncs[i]: 
                        newNodeData[j] = nodeData[j]-DiD0[i]
                    
        newData.append(newNodeData)

    return newData






