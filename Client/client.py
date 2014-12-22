import socket
import sys
import AcousticPipe
from SensorLocations import *

nodeinit()

d = raw_input("Please enter durration: ")

num_sensors = len(Nodes)

sensors = []

for i in range(num_sensors):
    
    # Create a TCP/IP socket
    sensors.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    # Connect the socket to the port where the server is listening
    IP = '192.168.2.10'+str(i)
    server_address = (IP,1234)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sensors[i].connect(server_address)

     # Send data
    message = d
    print >>sys.stderr, 'sending "%s"' % message
    sensors[i].sendall(message)

for i in range(num_sensors):
    data = ''
    while (len(data) < 1):
        data = sensors[i].recv(4096)
    
    print >>sys.stderr, 'received "%s"' % data
    sensors[i].close()
    fname = 's'+str(i)+'.txt'
    
    file=open(fname,"w")
    
    file.write(data)
    file.close()

AcousticPipe.run()





