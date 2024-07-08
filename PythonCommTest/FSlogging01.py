import socket
import datetime
from time import sleep
import winsound

from psychopy.hardware.keyboard import Keyboard

kb = Keyboard()

UDP_IP = "130.230.124.109"
UDP_PORT = 5005

# Output file path
myd = datetime.datetime.now()
fpath = r'C:\Users\Civit\Documents\Yuta_LFacmExpr\exprdata\{}.txt'.format(myd.strftime('%Y%m%d-%H%M%S'))
print(fpath)

intvl = input('Enter the FrontSurfer loop process time (ms): ')

# Just create a file and close
with open(fpath,encoding='utf-8',mode='x') as fdat:
    fdat.write(intvl + ' = Entered FrontSurfer loop process time\n')
    fdat.write('Date Time C1p1 C1m1 C20 C2p2 C2m2 C3p1 C3m1 C3p3 C3m3 C40\n')

zerokeyctr = 0
try:
    fdat = open(fpath,encoding='utf-8',mode='a') # Reopen the file in 'append' mode
    print('Wavefront data receiving & recording...')

    # Setup communication to FrontSurfer
    sock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    sock.settimeout(0.0) # Set socket in non-blocking mode 
    # print('Socket timeout = {}'.format(sock.gettimeout()))

    while True:
        try:
            sleep(0.05)
            # Must be in non-blocking mode (timeout of 0.0 s), throws BlockingIOError when nothing in the buffer
            # Assuming there is no chattering (data is sent from FrontSurfer ONLY ONE in every 1-2 seconds)
            # If there will be, another while loop to read all pooled data out from buffer would be needed.
            receivedstrs = []
            while True:
                try:
                    dat = sock.recv(2048) 
                    receivedstrs.append(dat.decode('utf-8'))
                except BlockingIOError:
                    break
            if len(receivedstrs) > 1:
                print(len(receivedstrs)) # Mostly zero, often one. Print to console if it is 2 or more (chattering likely happening)
            for thisstr in receivedstrs:
                fdat.write(thisstr)
            # if ctr > 100:
            #     break
            keys = kb.getKeys()
            if '0' in keys:
                zerokeyctr += 1
                if zerokeyctr > 4:
                    winsound.Beep(440,500)
                    break
        except BlockingIOError:
            print('Received nothing')
            pass
    
    print('Wavefront data recording stopped')
    sleep(2)
    fdat.close()
except FileExistsError:
    print("ERROR: File exists!")
except Exception as e:
    print(e)
    fdat.close()