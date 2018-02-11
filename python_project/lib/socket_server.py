import socket


address = ('127.0.0.1', 80)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
print 'socket established'
# remote_ip = socket.gethostbyname(web_site)
# print remote_ip

s.bind(address)  
s.listen(5)  
   
ss, addr = s.accept()  
print 'got connected from',addr  
 
count = 1
while True:
    ss.send('byebye')  
    ra = ss.recv(512)  
    print ra
    if "q" in ra:
        break  
   
ss.close()  
s.close()  
