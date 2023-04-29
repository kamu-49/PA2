from socket import *
from sys import *
import time
import signal
import random

##### DECLARATIONS #####
byte = 8
letter = [byte]
sequence_number = [32]
data_packet = [len(letter) + len(sequence_number)]
data_packet_size = len(data_packet)
timeout = 0.5
holder = 0


##### SENDER #####
def sender(sp, pp, ws, tt, tv):
    print("hello. inside sender")
    ### Declarations
    seq_index = 0

    ### sock init
    sa = ('localhost',sp)
    ra = ('localhost', pp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(sa)
    buffer = [data_packet_size*ws]

    ## test 1 ##
    print("current address: ", sa)
    print("test1")
    while True:
        hold, addr = sock.recvfrom(1024)
        print(hold)
        h = hold.decode()
        print(h)
        break
    ## test 1 done ##

    ## test 2 ##
    msg = input("sender> ")
    mmsg = "the message received was: " + msg
    sock.sendto(mmsg.encode(), ra)
    ## test 2  done ##

    ## test 3 ##
    test3 = []
    for i in msg:
        test3.append(i)
    t3h = 0
    while t3h < len(test3):
        sock.sendto(test3[t3h].encode(), ra)
        t3h += 1
        if t3h == len(test3):
            nah = b"finished"
            sock.sendto(nah, ra)
            break
    ## test 3 done ##
    print("shutting down sender...")
    time.sleep(3)

def receiver(rp, pp, ws, tt, tv):
    print("hello. in receiver")
    seq_index = 0

    ### sock init
    sa = ('localhost',pp)
    ra = ('localhost', rp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ra)
    buffer = [data_packet_size*ws]

    ## test 1 ##
    print("sending to: ", sa)
    print("Test1")
    hi = b"hi. receiver to sender"
    sock.sendto(hi, sa)
    ## test 1 done ##

     ## test 2 ##
    while True:
        s, a = sock.recvfrom(1024)
        print(s)
        print(s.decode())
        break
    ## test 2 done ##
    while True:
        a, b = sock.recvfrom(1024)
        if(a.decode() == "finished"):
            print("we done here chief")
            break
        else:
            print("Received: ", a.decode())
    ## test 3 done ##
    print("shutting down receiver...")
    time.sleep(3)

if __name__ == "__main__":
    sp = int(argv[1])
    pp = int(argv[2])
    ws = int(argv[3])
    pt = argv[4]
    pn = float(argv[5])

    mp = int((sp + pp)/ 2)
    s = socket(AF_INET, SOCK_DGRAM)
    time.sleep(0.5)
    try:
        print("attempting bind...")
        s.bind(('localhost',mp))
        print("no sender yet")
        sender(sp,pp,ws,pt,pn)
    except OSError as e:
        print("sender already alive")
        s.close()
        time.sleep(5)
        receiver(sp,pp,ws,pt,pn)