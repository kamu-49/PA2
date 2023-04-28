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
def sender(self_port, peer_port, window_size, timeout_type, timeout_value):
    print("hello. inside sender")
    ### Declarations
    sp = self_port
    rp = peer_port
    ws = window_size
    tt = timeout_type
    tv = timeout_value
    seq_index = 0

    ### sock init
    sa = ('',sp)
    ra = ('', rp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(sa)
    buffer = [data_packet_size*ws]

    ## test 1 ##
    print("current address: ", sa)
    print("test1")
    hold, addr = sock.recvfrom(1024)
    h = hold.decode()
    print(h)

    print("shutting down sender")
    time.sleep(5)
    ## test 1 ##

def receiver(self_port, peer_port, window_size, timeout_type, timeout_value):
    print("hello. in receiver")
    rp = self_port
    sp = peer_port
    ws = window_size
    tt = timeout_type
    tv = timeout_value
    seq_index = 0

    ### sock init
    sa = ('',sp)
    ra = ('', rp)
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ra)
    buffer = [data_packet_size*ws]
    ma = ('', (int((sp+rp)/2)))

    ## test 1 ##
    print("sending to: ", sa)
    print("Test1")
    hi = "hi. receiver to sender"
    sock.sendto(hi.encode(), sa)
    print("shutting down receiver")
    time.sleep(5)

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
        s.bind(('',mp))
        print("no sender yet")
        sender(sp,pp,ws,pt,pn)
    except OSError as e:
        print("sender already alive")
        s.close()
        time.sleep(5)
        receiver(sp,pp,ws,pt,pn)