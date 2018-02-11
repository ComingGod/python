import socket
import sys
#TCP_IP = '127.0.0.1'
#zebu11
#TCP_IP = '10.81.19.1'
#zebu13
#TCP_IP = '10.81.19.3'
#zebu21
TCP_IP = '127.0.0.1'
#zebu31
#TCP_IP = '10.81.19.11'
TCP_PORT = 10010
BUFFER_SIZE = 512
MESSAGE = "Hello, World!"

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket()
s.connect((TCP_IP, TCP_PORT))
# s.send(MESSAGE)
try: 
    with open('result/test.txt', 'w+') as f:
        while True:
            data = s.recv(BUFFER_SIZE)
            print data
            sys.stdout.write(data)
            sys.stdout.flush()
            f.write(data)
            s.send('haha')
except:
    print "file operation error"
  
s.close()
