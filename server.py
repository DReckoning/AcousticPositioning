import socket
import sys
import subprocess

IP = '192.168.2.10'
if (len(sys.argv) == 2):
    IP = IP + sys.argv[1]
else:
    print 'Error please enter the Sensor Number!'


def run(runlen):
    if (runlen < 1 or runlen > 99999):
        return 'ERROR INVALID RUNLEN'
    durr = str(runlen)
    print durr
    try:
#    subprocess.call(['cd','Desktop'])
        print 'Recording'
        subprocess.call(['arecord','-d',durr,'-f','cd','-c','1','run.wav'])
        print 'Converting'
        subprocess.call(['python','wtt.py','run.wav'])
        print 'PULSE'
        subprocess.call(['./pulse'])
    finally:
        print 'ERROR'
        
    file = open('s06000_times.txt','r')

    return file.read()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (IP, 1234)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'connection from', client_address


        
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                returndata = run(int(data))
                
                connection.sendall(returndata)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break
            
    finally:
        # Clean up the connection
        connection.close()

sock.close()
