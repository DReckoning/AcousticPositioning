import fastSpatial as spatial

Nodes = []

SyncNode = []

def nodeinit():
    if len(Nodes) < 1:
        
        # CHANGE THESE \/
        Nodes.append(spatial.Node(0,4.37,0)) #s0
        Nodes.append(spatial.Node(8.24,4.37,0)) #s1
        Nodes.append(spatial.Node(8.24,0,0)) #s2
        Nodes.append(spatial.Node(0,0,0)) #s3

        SyncNode.append(spatial.Node(4.51,4.37,0))

        # CHANGE THESE /\

