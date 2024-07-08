import socket
import time

UDP_IP = "192.168.1.2"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

with open('data.txt', mode='w', encoding='utf-8') as txtfile:
    pass

ctr = 0

while True:
    time.sleep(0.1)
    data, addr = sock.recvfrom(1024)
    thisstr = data.decode('utf-8')
    print("Received message: %s" % thisstr)
    # print(type(data))
    # print(type(str(data)))
    txtfile.write(thisstr)
    txtfile.flush()
    ctr += 1
    if ctr > 99:
        break
